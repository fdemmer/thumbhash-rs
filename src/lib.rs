use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use thumbhash;

/// Largest width and height supported by ThumbHash.
const MAX_SIZE: usize = 100;

/// Encodes an RGBA image to a ThumbHash. RGB should not be premultiplied by A.
///
/// :param width: The width of the input image. Must be at most 100 pixels.
/// :param height: The height of the input image. Must be at most 100 pixels.
/// :param rgba: The pixels of the input image, row by row, with 4 bytes (R, G, B, A)
///     per pixel. Must be exactly ``width * height * 4`` bytes long.
/// :returns: The ThumbHash.
/// :raises ValueError: If ``width`` or ``height`` is larger than 100, or ``rgba``
///     has the wrong length.
#[pyfunction(name = "rgba_to_thumb_hash")]
fn py_rgba_to_thumb_hash<'py>(
    py: Python<'py>,
    width: usize,
    height: usize,
    rgba: &[u8],
) -> PyResult<Bound<'py, PyBytes>> {
    // The thumbhash crate asserts on these, which would surface as a PanicException.
    if width > MAX_SIZE || height > MAX_SIZE {
        return Err(PyValueError::new_err(format!(
            "width and height must be at most {MAX_SIZE}, got {width}x{height}"
        )));
    }
    let expected = width * height * 4;
    if rgba.len() != expected {
        return Err(PyValueError::new_err(format!(
            "rgba must be width * height * 4 = {expected} bytes long, got {}",
            rgba.len()
        )));
    }
    let hash = py.detach(|| thumbhash::rgba_to_thumb_hash(width, height, rgba));
    Ok(PyBytes::new(py, &hash))
}

/// Decodes a ThumbHash to an RGBA image. RGB is not premultiplied by A.
///
/// :param hash: The bytes of the ThumbHash.
/// :returns: The width, height, and pixels of the rendered placeholder image, as
///     ``(width, height, rgba)``. The pixels are row by row, with 4 bytes
///     (R, G, B, A) per pixel.
/// :raises ValueError: If the hash is invalid or malformed.
#[pyfunction(name = "thumb_hash_to_rgba")]
fn py_thumb_hash_to_rgba<'py>(
    py: Python<'py>,
    hash: &[u8],
) -> PyResult<(usize, usize, Bound<'py, PyBytes>)> {
    let (width, height, rgba) =
        py.detach(|| thumbhash::thumb_hash_to_rgba(hash))
            .map_err(|_| {
                PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid or malformed thumbhash")
            })?;
    Ok((width, height, PyBytes::new(py, &rgba)))
}

/// Extracts the average color from a ThumbHash. RGB is not premultiplied by A.
///
/// :param hash: The bytes of the ThumbHash.
/// :returns: The average color as ``(r, g, b, a)``. Each value ranges from 0 to 1.
/// :raises ValueError: If the hash is invalid or malformed.
#[pyfunction(name = "thumb_hash_to_average_rgba")]
fn py_thumb_hash_to_average_rgba(py: Python, hash: &[u8]) -> PyResult<(f32, f32, f32, f32)> {
    py.detach(|| thumbhash::thumb_hash_to_average_rgba(hash))
        .map_err(|_| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid or malformed thumbhash")
        })
}

/// Extracts the approximate aspect ratio of the original image.
///
/// :param hash: The bytes of the ThumbHash.
/// :returns: The approximate aspect ratio (i.e. width / height).
/// :raises ValueError: If the hash is invalid or malformed.
#[pyfunction(name = "thumb_hash_to_approximate_aspect_ratio")]
fn py_thumb_hash_to_approximate_aspect_ratio(py: Python, hash: &[u8]) -> PyResult<f32> {
    py.detach(|| thumbhash::thumb_hash_to_approximate_aspect_ratio(hash))
        .map_err(|_| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid or malformed thumbhash")
        })
}

/// Fast ThumbHash encoding and decoding, implemented in Rust.
///
/// See https://evanw.github.io/thumbhash/ for details on the ThumbHash format.
#[pymodule]
fn _thumbhash(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_rgba_to_thumb_hash, m)?)?;
    m.add_function(wrap_pyfunction!(py_thumb_hash_to_rgba, m)?)?;
    m.add_function(wrap_pyfunction!(py_thumb_hash_to_average_rgba, m)?)?;
    m.add_function(wrap_pyfunction!(
        py_thumb_hash_to_approximate_aspect_ratio,
        m
    )?)?;
    Ok(())
}

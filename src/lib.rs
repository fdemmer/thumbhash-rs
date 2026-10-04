use pyo3::prelude::*;
use pyo3::types::PyBytes;
use thumbhash;

#[pyfunction(name = "rgba_to_thumb_hash")]
fn py_rgba_to_thumb_hash<'py>(
    py: Python<'py>,
    width: usize,
    height: usize,
    rgba: &[u8],
) -> Bound<'py, PyBytes> {
    let hash = py.allow_threads(|| thumbhash::rgba_to_thumb_hash(width, height, rgba));
    PyBytes::new_bound(py, &hash)
}

#[pyfunction(name = "thumb_hash_to_rgba")]
fn py_thumb_hash_to_rgba<'py>(
    py: Python<'py>,
    hash: &[u8],
) -> PyResult<(usize, usize, Bound<'py, PyBytes>)> {
    let (width, height, rgba) = py
        .allow_threads(|| thumbhash::thumb_hash_to_rgba(hash))
        .map_err(|_| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid or malformed thumbhash")
        })?;
    Ok((width, height, PyBytes::new_bound(py, &rgba)))
}

#[pyfunction(name = "thumb_hash_to_average_rgba")]
fn py_thumb_hash_to_average_rgba(py: Python, hash: &[u8]) -> PyResult<(f32, f32, f32, f32)> {
    py.allow_threads(|| thumbhash::thumb_hash_to_average_rgba(hash))
        .map_err(|_| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid or malformed thumbhash")
        })
}

#[pyfunction(name = "thumb_hash_to_approximate_aspect_ratio")]
fn py_thumb_hash_to_approximate_aspect_ratio(py: Python, hash: &[u8]) -> PyResult<f32> {
    py.allow_threads(|| thumbhash::thumb_hash_to_approximate_aspect_ratio(hash))
        .map_err(|_| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid or malformed thumbhash")
        })
}

#[pymodule]
fn fast_thumbhash(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_rgba_to_thumb_hash, m)?)?;
    m.add_function(wrap_pyfunction!(py_thumb_hash_to_rgba, m)?)?;
    m.add_function(wrap_pyfunction!(py_thumb_hash_to_average_rgba, m)?)?;
    m.add_function(wrap_pyfunction!(
        py_thumb_hash_to_approximate_aspect_ratio,
        m
    )?)?;
    Ok(())
}

const { validationResult } = require('express-validator');
const Genero = require('../models/genero');

// Obtener un género por su ID
exports.getGenero = async (req, res) => {
  try {
    const genero = await Genero.findOne({ _id: req.params.id, activo: true });
    
    if (!genero) {
      return res.status(404).json({ mensaje: 'Género no encontrado o inactivo' });
    }
    
    res.json({
      genero_id: genero._id,
      nombre: genero.nombre
    });
  } catch (error) {
    console.error('Error al obtener género:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Obtener todos los géneros
exports.getGeneros = async (req, res) => {
  try {
    const generos = await Genero.find({ activo: true });
    
    const resultado = generos.map(genero => ({
      genero_id: genero._id,
      nombre: genero.nombre
    }));
    
    res.json(resultado);
  } catch (error) {
    console.error('Error al obtener géneros:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Crear un género
exports.createGenero = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { nombre } = req.body;

  try {
    // Verificar si ya existe un género con el mismo nombre
    let generoExistente = await Genero.findOne({ nombre, activo: true });
    if (generoExistente) {
      return res.status(400).json({ mensaje: 'Ya existe un género con ese nombre' });
    }

    // Crear género
    const genero = new Genero({
      nombre
    });

    // Guardar género
    await genero.save();

    // Respuesta
    res.status(201).json({
      genero_id: genero._id,
      nombre: genero.nombre,
      mensaje: 'Género creado con éxito'
    });
  } catch (error) {
    console.error('Error al crear género:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Actualizar un género
exports.updateGenero = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { nombre } = req.body;

  try {
    // Verificar si el género existe
    let genero = await Genero.findOne({ _id: req.params.id, activo: true });
    
    if (!genero) {
      return res.status(404).json({ mensaje: 'Género no encontrado o inactivo' });
    }

    // Verificar si ya existe otro género con el mismo nombre
    let generoExistente = await Genero.findOne({ 
      nombre, 
      _id: { $ne: req.params.id },
      activo: true
    });
    
    if (generoExistente) {
      return res.status(400).json({ mensaje: 'Ya existe otro género con ese nombre' });
    }

    // Actualizar género
    genero = await Genero.findByIdAndUpdate(
      req.params.id,
      { $set: { nombre } },
      { new: true }
    );

    // Respuesta
    res.json({
      resultado: 1,
      mensaje: 'Género actualizado con éxito'
    });
  } catch (error) {
    console.error('Error al actualizar género:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Eliminar un género (desactivar)
exports.deleteGenero = async (req, res) => {
  try {
    // Verificar si el género existe
    let genero = await Genero.findOne({ _id: req.params.id, activo: true });
    
    if (!genero) {
      return res.status(404).json({ mensaje: 'Género no encontrado o inactivo' });
    }

    // Desactivar género
    genero = await Genero.findByIdAndUpdate(
      req.params.id,
      { $set: { activo: false } },
      { new: true }
    );

    // Respuesta
    res.json({
      resultado: 1,
      mensaje: 'Género eliminado con éxito (desactivado)'
    });
  } catch (error) {
    console.error('Error al eliminar género:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};
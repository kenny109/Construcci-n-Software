const { validationResult } = require('express-validator');
const Autor = require('../models/autor');
const Libro = require('../models/libro');

// Obtener un autor por su ID
exports.getAutor = async (req, res) => {
  try {
    const autor = await Autor.findOne({ _id: req.params.id, activo: true });
    
    if (!autor) {
      return res.status(404).json({ mensaje: 'Autor no encontrado o inactivo' });
    }
    
    res.json({
      autor_id: autor._id,
      nombre: autor.nombre,
      apellido: autor.apellido,
      nacionalidad: autor.nacionalidad,
      fecha_nacimiento: autor.fecha_nacimiento ? autor.fecha_nacimiento.toISOString().split('T')[0] : null
    });
  } catch (error) {
    console.error('Error al obtener autor:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Obtener todos los autores
exports.getAutores = async (req, res) => {
  try {
    const autores = await Autor.find({ activo: true });
    
    const resultado = autores.map(autor => ({
      autor_id: autor._id,
      nombre: autor.nombre,
      apellido: autor.apellido,
      nacionalidad: autor.nacionalidad,
      fecha_nacimiento: autor.fecha_nacimiento ? autor.fecha_nacimiento.toISOString().split('T')[0] : null
    }));
    
    res.json(resultado);
  } catch (error) {
    console.error('Error al obtener autores:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Obtener libros por autor
exports.getLibrosByAutor = async (req, res) => {
  try {
    const libros = await Libro.find({ 
      autores: req.params.id, 
      activo: true 
    }).select('_id titulo anio_publicacion');
    
    const resultado = libros.map(libro => ({
      libro_id: libro._id,
      titulo: libro.titulo,
      anio_publicacion: libro.anio_publicacion
    }));
    
    res.json(resultado);
  } catch (error) {
    console.error('Error al obtener libros por autor:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Crear un autor
exports.createAutor = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { nombre, apellido, nacionalidad, fecha_nacimiento } = req.body;

  try {
    // Crear autor
    const autor = new Autor({
      nombre,
      apellido,
      nacionalidad,
      fecha_nacimiento
    });

    // Guardar autor
    await autor.save();

    // Respuesta
    res.status(201).json({
      autor_id: autor._id,
      nombre: autor.nombre,
      apellido: autor.apellido,
      nacionalidad: autor.nacionalidad,
      fecha_nacimiento: autor.fecha_nacimiento ? autor.fecha_nacimiento.toISOString().split('T')[0] : null
    });
  } catch (error) {
    console.error('Error al crear autor:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Actualizar un autor
exports.updateAutor = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { nombre, apellido, nacionalidad, fecha_nacimiento } = req.body;

  try {
    // Verificar si el autor existe
    let autor = await Autor.findOne({ _id: req.params.id, activo: true });
    
    if (!autor) {
      return res.status(404).json({ mensaje: 'Autor no encontrado o inactivo' });
    }

    // Actualizar autor
    const autorActualizado = {};
    if (nombre) autorActualizado.nombre = nombre;
    if (apellido) autorActualizado.apellido = apellido;
    if (nacionalidad !== undefined) autorActualizado.nacionalidad = nacionalidad;
    if (fecha_nacimiento !== undefined) autorActualizado.fecha_nacimiento = fecha_nacimiento;

    autor = await Autor.findByIdAndUpdate(
      req.params.id,
      { $set: autorActualizado },
      { new: true }
    );

    // Respuesta
    res.json({
      resultado: 1,
      mensaje: 'Autor actualizado con éxito'
    });
  } catch (error) {
    console.error('Error al actualizar autor:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Eliminar un autor (desactivar)
exports.deleteAutor = async (req, res) => {
  try {
    // Verificar si el autor existe
    let autor = await Autor.findOne({ _id: req.params.id, activo: true });
    
    if (!autor) {
      return res.status(404).json({ mensaje: 'Autor no encontrado o inactivo' });
    }

    // Desactivar autor
    autor = await Autor.findByIdAndUpdate(
      req.params.id,
      { $set: { activo: false } },
      { new: true }
    );

    // Respuesta
    res.json({
      resultado: 1,
      mensaje: 'Autor eliminado con éxito (desactivado)'
    });
  } catch (error) {
    console.error('Error al eliminar autor:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};
const { validationResult } = require('express-validator');
const Libro = require('../models/libro');
const Autor = require('../models/autor');
const Genero = require('../models/genero');

// Obtener un libro por su ID
exports.getLibro = async (req, res) => {
  try {
    const libro = await Libro.findOne({ _id: req.params.id, activo: true })
      .populate('autores', 'nombre apellido')
      .populate('generos', 'nombre');
    
    if (!libro) {
      return res.status(404).json({ mensaje: 'Libro no encontrado o inactivo' });
    }
    
    const resultado = {
      libro_id: libro._id,
      titulo: libro.titulo,
      anio_publicacion: libro.anio_publicacion,
      autores: libro.autores.map(autor => ({
        autor_id: autor._id,
        nombre: autor.nombre,
        apellido: autor.apellido
      })),
      generos: libro.generos.map(genero => ({
        genero_id: genero._id,
        nombre: genero.nombre
      }))
    };
    
    res.json(resultado);
  } catch (error) {
    console.error('Error al obtener libro:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Obtener todos los libros
exports.getLibros = async (req, res) => {
  try {
    const libros = await Libro.find({ activo: true })
      .populate('autores', 'nombre apellido')
      .populate('generos', 'nombre');
    
    const resultado = libros.map(libro => ({
      libro_id: libro._id,
      titulo: libro.titulo,
      anio_publicacion: libro.anio_publicacion,
      autores: libro.autores.map(autor => ({
        autor_id: autor._id,
        nombre: autor.nombre,
        apellido: autor.apellido
      })),
      generos: libro.generos.map(genero => ({
        genero_id: genero._id,
        nombre: genero.nombre
      }))
    }));
    
    res.json(resultado);
  } catch (error) {
    console.error('Error al obtener libros:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Obtener autores por libro
exports.getAutoresByLibro = async (req, res) => {
  try {
    const libro = await Libro.findOne({ _id: req.params.id, activo: true })
      .populate('autores');
    
    if (!libro) {
      return res.status(404).json({ mensaje: 'Libro no encontrado o inactivo' });
    }
    
    const autores = libro.autores.map(autor => ({
      autor_id: autor._id,
      nombre: autor.nombre,
      apellido: autor.apellido,
      nacionalidad: autor.nacionalidad,
      fecha_nacimiento: autor.fecha_nacimiento ? autor.fecha_nacimiento.toISOString().split('T')[0] : null
    }));
    
    res.json(autores);
  } catch (error) {
    console.error('Error al obtener autores por libro:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Crear un libro
exports.createLibro = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { titulo, anio_publicacion, autores_ids, generos_ids } = req.body;

  try {
    // Verificar que todos los autores existan
    for (const autor_id of autores_ids) {
      const autorExistente = await Autor.findOne({ _id: autor_id, activo: true });
      if (!autorExistente) {
        return res.status(400).json({ mensaje: `El autor con ID ${autor_id} no existe o está inactivo` });
      }
    }

    // Verificar que todos los géneros existan
    if (generos_ids && generos_ids.length > 0) {
      for (const genero_id of generos_ids) {
        const generoExistente = await Genero.findOne({ _id: genero_id, activo: true });
        if (!generoExistente) {
          return res.status(400).json({ mensaje: `El género con ID ${genero_id} no existe o está inactivo` });
        }
      }
    }

    // Crear libro
    const libro = new Libro({
      titulo,
      anio_publicacion,
      autores: autores_ids,
      generos: generos_ids || []
    });

    // Guardar libro
    await libro.save();

    // Respuesta
    res.status(201).json({
      libro_id: libro._id,
      titulo: libro.titulo,
      anio_publicacion: libro.anio_publicacion,
      autores_ids: libro.autores,
      generos_ids: libro.generos,
      mensaje: 'Libro creado con éxito'
    });
  } catch (error) {
    console.error('Error al crear libro:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Actualizar un libro
exports.updateLibro = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { titulo, anio_publicacion, autores_ids, generos_ids } = req.body;

  try {
    // Verificar si el libro existe
    let libro = await Libro.findOne({ _id: req.params.id, activo: true });
    
    if (!libro) {
      return res.status(404).json({ mensaje: 'Libro no encontrado o inactivo' });
    }

    // Verificar que todos los autores existan
    if (autores_ids && autores_ids.length > 0) {
      for (const autor_id of autores_ids) {
        const autorExistente = await Autor.findOne({ _id: autor_id, activo: true });
        if (!autorExistente) {
          return res.status(400).json({ mensaje: `El autor con ID ${autor_id} no existe o está inactivo` });
        }
      }
    }

    // Verificar que todos los géneros existan
    if (generos_ids && generos_ids.length > 0) {
      for (const genero_id of generos_ids) {
        const generoExistente = await Genero.findOne({ _id: genero_id, activo: true });
        if (!generoExistente) {
          return res.status(400).json({ mensaje: `El género con ID ${genero_id} no existe o está inactivo` });
        }
      }
    }

    // Actualizar libro
    const libroActualizado = {};
    if (titulo) libroActualizado.titulo = titulo;
    if (anio_publicacion !== undefined) libroActualizado.anio_publicacion = anio_publicacion;
    if (autores_ids && autores_ids.length > 0) libroActualizado.autores = autores_ids;
    if (generos_ids) libroActualizado.generos = generos_ids;

    libro = await Libro.findByIdAndUpdate(
      req.params.id,
      { $set: libroActualizado },
      { new: true }
    );

    // Respuesta
    res.json({
      resultado: 1,
      mensaje: 'Libro actualizado con éxito'
    });
  } catch (error) {
    console.error('Error al actualizar libro:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor'});
  }
};

// Eliminar un libro (desactivar)
exports.deleteLibro = async (req, res) => {
    try {
      const { libro_id } = req.body;
      
      if (!libro_id) {
        return res.status(400).json({ error: 'ID de libro no proporcionado' });
      }
      
      // Verificar si el libro existe
      const libro = await Libro.findOne({ _id: libro_id, activo: true });
      if (!libro) {
        return res.status(404).json({ error: 'Libro no encontrado o inactivo' });
      }
      
      // Desactivar el libro en vez de eliminarlo
      await Libro.findByIdAndUpdate(libro_id, { activo: false });
      
      res.status(200).json({
        result: 1,
        message: 'Libro eliminado con éxito (desactivado)'
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  };
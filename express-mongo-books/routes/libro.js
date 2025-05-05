const express = require('express');
const router = express.Router();
const { check } = require('express-validator');
const libroController = require('../controllers/libro');
const auth = require('../middlewares/auth');

// Obtener todos los libros
router.get('/', libroController.getLibros);

// Obtener un libro específico
router.get('/:id', libroController.getLibro);

// Obtener autores de un libro
router.get('/:id/autores', libroController.getAutoresByLibro);

// Crear un libro (protegido con autenticación)
router.post('/', [
  auth,
  check('titulo', 'El título es obligatorio').not().isEmpty(),
  check('autores_ids', 'Debe proporcionar al menos un autor').isArray({ min: 1 })
], libroController.createLibro);

// Actualizar un libro (protegido con autenticación)
router.put('/:id', [
  auth,
  check('titulo', 'El título es obligatorio').not().isEmpty()
], libroController.updateLibro);

// Eliminar un libro (protegido con autenticación)
router.delete('/:id', auth, libroController.deleteLibro);

module.exports = router;
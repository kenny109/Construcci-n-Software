const express = require('express');
const router = express.Router();
const { check } = require('express-validator');
const autorController = require('../controllers/autor');
const auth = require('../middlewares/auth');

// Obtener todos los autores
router.get('/', autorController.getAutores);

// Obtener un autor específico
router.get('/:id', autorController.getAutor);

// Obtener libros de un autor
router.get('/:id/libros', autorController.getLibrosByAutor);

// Crear un autor (protegido con autenticación)
router.post('/', [
  auth,
  check('nombre', 'El nombre es obligatorio').not().isEmpty(),
  check('apellido', 'El apellido es obligatorio').not().isEmpty()
], autorController.createAutor);

// Actualizar un autor (protegido con autenticación)
router.put('/:id', [
  auth,
  check('nombre', 'El nombre es obligatorio').not().isEmpty(),
  check('apellido', 'El apellido es obligatorio').not().isEmpty()
], autorController.updateAutor);

// Eliminar un autor (protegido con autenticación)
router.delete('/:id', auth, autorController.deleteAutor);

module.exports = router;
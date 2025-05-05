const express = require('express');
const router = express.Router();
const { check } = require('express-validator');
const generoController = require('../controllers/genero');
const auth = require('../middlewares/auth');

// Obtener todos los géneros
router.get('/', generoController.getGeneros);

// Obtener un género específico
router.get('/:id', generoController.getGenero);

// Crear un género (protegido con autenticación)
router.post('/', [
  auth,
  check('nombre', 'El nombre es obligatorio').not().isEmpty()
], generoController.createGenero);

// Actualizar un género (protegido con autenticación)
router.put('/:id', [
  auth,
  check('nombre', 'El nombre es obligatorio').not().isEmpty()
], generoController.updateGenero);

// Eliminar un género (protegido con autenticación)
router.delete('/:id', auth, generoController.deleteGenero);

module.exports = router;
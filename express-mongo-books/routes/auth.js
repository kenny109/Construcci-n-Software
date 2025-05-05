const express = require('express');
const router = express.Router();
const { check } = require('express-validator');
const authController = require('../controllers/auth');

// Ruta para registrar un usuario
router.post('/registrar', [
  check('username', 'El nombre de usuario es obligatorio').not().isEmpty(),
  check('password', 'La contraseña debe tener al menos 6 caracteres').isLength({ min: 6 })
], authController.registrarUsuario);

// Ruta para iniciar sesión
router.post('/login', [
  check('username', 'El nombre de usuario es obligatorio').not().isEmpty(),
  check('password', 'La contraseña es obligatoria').exists()
], authController.loginUsuario);

module.exports = router;
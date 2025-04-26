const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { validationResult } = require('express-validator');
const Usuario = require('../models/usuario');

// Registrar usuario
exports.registrarUsuario = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { username, password } = req.body;

  try {
    // Verificar si el usuario ya existe
    let usuario = await Usuario.findOne({ username });
    if (usuario) {
      return res.status(400).json({ mensaje: 'El usuario ya existe' });
    }

    // Crear usuario
    usuario = new Usuario({
      username,
      password
    });

    // Encriptar contraseña
    const salt = await bcrypt.genSalt(10);
    usuario.password = await bcrypt.hash(password, salt);

    // Guardar usuario
    await usuario.save();

    // Respuesta
    res.status(201).json({
      usuario_id: usuario._id,
      username: usuario.username,
      mensaje: 'Usuario registrado con éxito'
    });
  } catch (error) {
    console.error('Error al registrar usuario:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};

// Iniciar sesión
exports.loginUsuario = async (req, res) => {
  // Validar los datos de entrada
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errores: errors.array() });
  }

  const { username, password } = req.body;

  try {
    // Verificar si el usuario existe
    const usuario = await Usuario.findOne({ username, activo: true });
    if (!usuario) {
      return res.status(401).json({ mensaje: 'Usuario no encontrado o inactivo' });
    }

    // Verificar contraseña
    const esCorrecta = await bcrypt.compare(password, usuario.password);
    if (!esCorrecta) {
      return res.status(401).json({ mensaje: 'Contraseña incorrecta' });
    }

    // Crear y firmar el token
    const payload = {
      id: usuario._id,
      username: usuario.username
    };

    jwt.sign(
      payload,
      process.env.JWT_SECRET,
      { expiresIn: '24h' },
      (error, token) => {
        if (error) throw error;
        res.json({
          token,
          mensaje: 'Inicio de sesión exitoso'
        });
      }
    );
  } catch (error) {
    console.error('Error al iniciar sesión:', error.message);
    res.status(500).json({ mensaje: 'Error en el servidor' });
  }
};
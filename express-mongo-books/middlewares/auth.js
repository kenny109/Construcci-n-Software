const jwt = require('jsonwebtoken');
const Usuario = require('../models/usuario');

const auth = async (req, res, next) => {
  try {
    // Verificar si hay un token en los headers
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ mensaje: 'Token no proporcionado' });
    }

    const token = authHeader.split(' ')[1];
    
    // Verificar el token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Buscar el usuario en la base de datos
    const usuario = await Usuario.findOne({ _id: decoded.id, activo: true });
    
    if (!usuario) {
      return res.status(401).json({ mensaje: 'Token inválido o expirado' });
    }
    
    // Agregar el usuario al request
    req.usuario = usuario;
    next();
  } catch (error) {
    console.error('Error en autenticación:', error.message);
    return res.status(401).json({ mensaje: 'Token inválido o expirado' });
  }
};

module.exports = auth;
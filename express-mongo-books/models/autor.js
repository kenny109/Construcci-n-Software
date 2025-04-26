const mongoose = require('mongoose');

const AutorSchema = new mongoose.Schema({
  nombre: {
    type: String,
    required: true
  },
  apellido: {
    type: String,
    required: true
  },
  nacionalidad: {
    type: String
  },
  fecha_nacimiento: {
    type: Date
  },
  activo: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Autor', AutorSchema);
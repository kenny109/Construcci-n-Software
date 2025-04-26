const mongoose = require('mongoose');

const LibroSchema = new mongoose.Schema({
  titulo: {
    type: String,
    required: true
  },
  anio_publicacion: {
    type: Number
  },
  autores: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Autor',
    required: true
  }],
  generos: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Genero'
  }],
  activo: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Libro', LibroSchema);
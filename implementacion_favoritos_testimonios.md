# Plan de Implementación: Favoritos, Testimonios y Mejoras de Perfil

Este plan detalla los pasos para implementar el sistema de favoritos, el sistema de testimonios/reseñas por pedido, y el rediseño funcional del perfil de usuario.

## 1. Configuración del Entorno y Base de Datos
- [ ] Activar entorno virtual `.venv`.
- [ ] Ejecutar migraciones para los nuevos modelos `Favorite` y `Testimonial`.

## 2. Sistema de Favoritos
- [ ] **Backend**: Crear una vista `toggle_favorite` que reciba un `product_id`.
- [ ] **URL**: Registrar la ruta en `apps/products/urls.py`.
- [ ] **Frontend (Cards)**: 
    - Actualizar el ícono de corazón en las tarjetas de producto.
    - Implementar AJAX para marcar/desmarcar sin recargar.
- [ ] **Frontend (Perfil)**: Añadir sección "Favoritos" que liste los productos guardados.

## 3. Sistema de Testimonios y Calificaciones
- [ ] **Backend**: Crear una vista `submit_testimonial` asociada a una orden.
- [ ] **Frontend (Perfil)**:
    - En la lista de pedidos, detectar órdenes procesadas/completadas sin testimonio.
    - Mostrar botón "Calificar Servicio".
    - Implementar un Modal con selección de estrellas y campo de texto.
- [ ] **Home**: (Opcional) Preparar sección para mostrar testimonios destacados.

## 4. Mejoras Finales de UI/UX
- [ ] Refinar transiciones en el perfil.
- [ ] Asegurar compatibilidad con modo oscuro en los nuevos componentes.

---
**Nota**: Se requiere la aprobación del usuario para proceder con la implementación técnica detallada.

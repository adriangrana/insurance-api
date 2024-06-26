#!/bin/bash

# Eliminar archivos de caché de Python
find . -type d -name "__pycache__" -exec rm -r {} +

# Eliminar archivos de caché de pytest
rm -rf .pytest_cache

# Eliminar archivos de cobertura
rm -rf htmlcov .coverage

# Eliminar archivos de caché de pip
rm -rf ~/.cache/pip

# Eliminar otros archivos de caché como .mypy_cache
rm -rf .mypy_cache

echo "Limpieza completada."

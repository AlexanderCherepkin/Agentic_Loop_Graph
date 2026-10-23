"""OpenAPI Documentation Specification."""
from typing import List, Dict, Any


class OpenAPISpec:
    """Generate comprehensive OpenAPI documentation."""

    def __init__(self):
        self.components = {
            "schemas": {},
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
        }

    def add_parameter(
        self, path: str, operation_id: str, param_name: str, required: bool = True
    ):
        """Add request parameter."""
        return {
            "name": param_name,
            "in": "path" if "id" in param_name else "query",
            "required": required,
            "schema": {"type": "string"},
        }

    def add_header(self, header_name: str = "X-Request-ID"):
        """Add response header."""
        return {
            "name": header_name,
            "description": "Unique identifier for the request",
            "schema": {"type": "string"},
        }


# Figma API Endpoints Documentation

FIGMA_ENDPOINTS = [
    {
        "path": "/api/figma/export",
        "method": "POST",
        "summary": "Экспорт дизайна из Figma",
        "description": "Создает экспорт изображения из указанного фрейма Figma в различных форматах.",
        "parameters": [
            {"name": "file_key", "in": "path", "required": True},
            {"name": "node_id", "in": "query", "required": False},
            {"name": "format", "in": "query", "required": False, "default": "png"},
            {"name": "scale", "in": "query", "required": False, "default": 1},
        ],
        "responses": {
            "200": {"description": "Успешный экспорт изображения", "content": {"image/png": {}}},
            "400": {"description": "Некорректные параметры"},
        },
    },
    {
        "path": "/api/figma/nodes",
        "method": "POST",
        "summary": "Получение структуры узлов",
        "description": "Извлекает полную иерархию узлов из Figma файла.",
        "parameters": [
            {"name": "file_key", "in": "path", "required": True},
            {"name": "depth", "in": "query", "required": False, "default": 3},
        ],
        "responses": {
            "200": {"description": "Структура узлов JSON", "content": {"application/json": {}}},
            "401": {"description": "Неавторизованный доступ"},
        },
    },
    {
        "path": "/api/figma/styles",
        "method": "GET",
        "summary": "Список стилей файла",
        "description": "Получает все сохраненные стили (текст, эффекты, компоненты).",
        "parameters": [
            {"name": "file_key", "in": "path", "required": True},
            {"name": "type", "in": "query", "required": False, "enum": ["text", "effect", "component"]},
        ],
        "responses": {
            "200": {"description": "Список стилей JSON", "content": {"application/json": {}}},
        },
    },
]

WORKFLOW_ENDPOINTS = [
    {
        "path": "/api/workflows/{workflow_id}",
        "method": "GET",
        "summary": "Статус воркфлоу",
        "description": "Получить текущий статус выполнения воркфлоу.",
        "parameters": [{"name": "workflow_id", "in": "path", "required": True}],
        "responses": {
            "200": {"description": "Статус воркфлоу"},
            "404": {"description": "Воркфлоу не найден"},
        },
    },
]

AGENTS_ENDPOINTS = [
    {
        "path": "/api/agents/process",
        "method": "POST",
        "summary": "Обработка данных агентами",
        "description": "Передача данных на обработку через агентную систему.",
        "parameters": [
            {"name": "data", "in": "body", "required": True, "schema": {"type": "object"}},
        ],
        "responses": {
            "200": {"description": "Результат обработки"},
            "500": {"description": "Ошибка агентов"},
        },
    },
]

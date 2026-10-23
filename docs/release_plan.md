# Release Plan: Figma Export API & Agentic Loop Integration

## Version History

| Версия | Функциональность | Приоритет | Статус |
|--------|------------------|-----------|--------|
| 0.1.0 | Базовый контроллер + PNG экспорт | 🔴 High | ✅ Completed |
| 0.2.0 | Добавление всех форматов экспорта (SVG, PDF) | 🟠 Medium | ⏳ In Progress |
| 0.3.0 | Интеграция с Agentic Loop Graph | 🟠 Medium | ⏳ Planned |
| 0.4.0 | Полное тестирование + документация | 🟢 Low | ⏳ Planned |

## Release Notes

### v0.1.0 - Базовый релиз
- ✅ FastAPI контроллер для Figma API
- ✅ Экспорт изображений в PNG формате
- ✅ JWT аутентификация
- ✅ Базовое логирование
- ✅ OpenAPI документация (Swagger UI)

### v0.2.0 - Расширение форматов
- 🔄 Добавление SVG экспорта
- 🔄 Поддержка PDF экспорта для макетов
- 🔄 Оптимизация качества изображений
- 🔄 Батированный экспорт нескольких фреймов

### v0.3.0 - Agentic Loop Integration
- 🔲 Интеграция с workflow_manager.py
- 🔲 Автоматическая обработка через агентов
- 🔲 Параллельная обработка запросов
- 🔲 Умное кэширование результатов

### v0.4.0 - Стабильность и документация
- 📝 Полный набор unit тестов (coverage > 90%)
- 📝 Интеграционные тесты с Figma API
- 📝 Load testing под нагрузкой
- 📝 Production hardening

## Deployment Checklist

### Pre-release
- [ ] Code review всех изменений
- [ ] Unit тесты проходят успешно
- [ ] Integration тесты завершены
- [ ] Security audit (OWASP Top 10)
- [ ] Performance benchmarks задокументированы

### Release Day
- [ ] Create release branch
- [ ] Tag version in git
- [ ] Deploy to staging environment
- [ ] Smoke tests on staging
- [ ] Deploy to production
- [ ] Monitor error rates (Sentry)
- [ ] Verify Prometheus metrics

## Rollback Plan

Если критическая ошибка обнаружена после деплоя:

1. Откат версии через Docker Compose: `docker-compose rollback`
2. Восстановление из backup базы данных
3. Откат конфигурации через Ansible/Terraform
4. Уведомление stakeholders об инциденте

## Metrics Dashboard

Ключевые метрики для мониторинга:

```yaml
- http_request_total (count)
- figma_api_calls_total (count)  
- http_request_duration_seconds (histogram)
- active_workflows_total (gauge)
- exported_images_total (gauge)
- Error rate < 1%
- P95 latency < 2s
```

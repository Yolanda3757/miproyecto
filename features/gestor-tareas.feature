Feature: Gestor de Tareas
  Para organizar mis pendientes
  Como usuario del sistema
  Quiero poder crear y visualizar tareas

  Scenario: Crear tarea con datos válidos
    Given el usuario está en la pantalla de gestor de tareas
    When ingresa título "Comprar leche" y descripción "Ir al supermercado"
    And pulsa el botón "Crear tarea"
    Then la tarea aparece en la lista de tareas

  Scenario: Intentar crear tarea sin título
    Given el usuario está en la pantalla de gestor de tareas
    When deja vacío el campo título y escribe descripción "Detalles de la tarea"
    And pulsa el botón "Crear tarea"
    Then aparece un mensaje de error indicando que el título es obligatorio

  Scenario: Visualizar lista de tareas
    Given existen tareas creadas previamente
    When el usuario abre la pantalla de gestor de tareas
    Then se muestran todas las tareas en la lista

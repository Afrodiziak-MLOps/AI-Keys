# Урок 2: Списки и циклы

# Создаём список любимых инструментов
tools = ["Ollama", "Docker", "Python", "VS Code", "WSL2"]

print("Мои любимые инструменты для MLOps:")
# Цикл for перебирает список по одному элементу
for tool in tools:
    print("-", tool)

# Считаем, сколько всего инструментов
count = len(tools)
print("Всего инструментов:", count)

# Добавляем новый инструмент в список
new_tool = input("Какой ещё инструмент добавить? ")
tools.append(new_tool)

print("Обновлённый список:")
for tool in tools:
    print("-", tool)
print("Теперь инструментов:", len(tools))
import json
import os


class SimpleDB:
    def __init__(self):
        self.documents = []

    def add(self, document):
        if 'id' not in document:
            document['id'] = len(self.documents) + 1

        for doc in self.documents:
            if doc['id'] == document['id']:
                print(f"Помилка: ID {document['id']} вже існує.")
                return False

        self.documents.append(document)
        return True

    def get_nested_value(self, doc, field_path):
        keys = field_path.split('.')
        val = doc
        try:
            for k in keys:
                if isinstance(val, dict):
                    val = val.get(k)
                else:
                    return None
            return val
        except Exception:
            return None

    def find(self, field, operator, value):
        results = []
        for doc in self.documents:
            target_val = self.get_nested_value(doc, field)

            try:
                if operator == "==":
                    if target_val == value: results.append(doc)
                elif operator == ">":
                    if target_val > value: results.append(doc)
                elif operator == "<":
                    if target_val < value: results.append(doc)
                elif operator == ">=":
                    if target_val >= value: results.append(doc)
                elif operator == "<=":
                    if target_val <= value: results.append(doc)
                elif operator == "exists":
                    if target_val is not None: results.append(doc)
                elif operator == "in_list":
                    if isinstance(target_val, list) and value in target_val:
                        results.append(doc)
            except TypeError:
                continue
        return results

    def delete_by_id(self, doc_id):
        initial_len = len(self.documents)
        self.documents = [d for d in self.documents if d.get('id') != doc_id]
        return len(self.documents) < initial_len

    def update(self, doc_id, field, new_value):
        for doc in self.documents:
            if doc.get('id') == doc_id:
                doc[field] = new_value
                return True
        return False

    def aggregate(self, operation, field):
        values = []
        for doc in self.documents:
            val = self.get_nested_value(doc, field)
            if isinstance(val, (int, float)):
                values.append(val)

        if not values and operation != "count":
            return "Немає числових даних для агрегації"

        if operation == "count": return len(self.documents)
        if operation == "sum": return sum(values)
        if operation == "avg": return sum(values) / len(values) if values else 0
        if operation == "min": return min(values)
        if operation == "max": return max(values)

    def group_by(self, field):
        groups = {}
        for doc in self.documents:
            key = str(self.get_nested_value(doc, field))
            if key not in groups:
                groups[key] = []
            groups[key].append(doc)
        return groups

    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=4, ensure_ascii=False)

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
            return True
        return False

def main():
    db = SimpleDB()

    while True:
        print("\n Спрощена JSON БД ")
        print("1. Додати (JSON)")
        print("2. Показати всі")
        print("3. Пошук (поле оператор значення)")
        print("4. Агрегація (count/sum/avg/min/max)")
        print("5. Групування")
        print("6. Зберегти/Завантажити")
        print("0. Вихід")

        choice = input("Оберіть дію: ")

        if choice == "1":
            try:
                raw_json = input("Введіть документ у форматі JSON: ")
                data = json.loads(raw_json)
                if db.add(data): print("Додано!")
            except Exception as e:
                print("Помилка JSON:", e)

        elif choice == "2":
            for d in db.documents: print(d)

        elif choice == "3":
            f = input("Поле (н-ад: age або address.city): ")
            op = input("Оператор (==, >, <, exists, in_list): ")
            v = input("Значення (для чисел введіть число): ")
            if v.isdigit():
                v = int(v)
            elif v.lower() == "true":
                v = True
            elif v.lower() == "false":
                v = False

            res = db.find(f, op, v)
            print(f"Знайдено ({len(res)}):", res)

        elif choice == "4":
            op = input("Операція (count, sum, avg, min, max): ")
            f = input("Поле: ")
            print("Результат:", db.aggregate(op, f))

        elif choice == "5":
            f = input("Поле для групування: ")
            groups = db.group_by(f)
            for k, v in groups.items():
                print(f"Група {k}: {len(v)} документів")

        elif choice == "6":
            cmd = input("save або load? ")
            fname = input("Назва файлу: ")
            if cmd == "save":
                db.save(fname)
            else:
                db.load(fname)
            print("Виконано.")

        elif choice == "0":
            break


if __name__ == "__main__":
    main()
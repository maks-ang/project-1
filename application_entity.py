class ApplicationRecord:
    def __init__(self, application_id, customer_name):
        self.id = application_id
        self.customer_name = customer_name
        self.status = "new"
        self.history = []

    def change_status(self, new_status):
        status_list = ["new", "processing", "done"]
        if new_status not in status_list:
            raise ValueError("Неизвестный статус")
        if self.status == new_status:
            return
        else:
            self.status = new_status
            self.history.append(new_status)


record = ApplicationRecord(1, "Макс")

print(record.id)             # 1
print(record.customer_name)  # Макс
print(record.status)         # new
print(record.history)        # []

record.change_status("processing")
record.change_status("done")

print(record.status)   # done
print(record.history)  # ['processing', 'done']


def by_hostname(server):
    return server.hostname

def by_load(server):
    return server.calculate_load()

def by_load_desc(server):
    return -server.calculate_load()

def is_active(server):
    return server.status == "active"

def is_web_server(server):
    return server.__class__.__name__ == "WebServer"

def has_high_load(threshold):
    def filter_fn(item):
        return item.calculate_load() > threshold
    return filter_fn

class LoadSortStrategy:
    def __init__(self, reverse=False):
        self.reverse = reverse
    def __call__(self, server):
        load = server.calculate_load()
        return -load if self.reverse else load

def log_server(server):
    print(f"  {server.hostname}: {server.calculate_load():.1f}%")
    return server
import time

from providers import golem

start = time.time()
data = golem.get()
end = time.time()
print(f"Retrieved {len(data)} items in {(end - start):.1f} seconds")

assert len(data) > 0, "No articles returned"
for article in data:
    for key in ['mainText', 'redirectionUrl', 'titleText', 'uid', 'updateDate']:
        assert key in article, f"Missing key {key} in an article"

print("All tests passed")

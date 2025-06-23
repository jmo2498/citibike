from scripts.pipeline import run_pipeline

def station_status_entrypoint(request):
    run_pipeline()
    return "✅ Pipeline completed", 200

# 🔧 Local testing
if __name__ == "__main__":
    class DummyRequest:
        args = {}

    msg, code = station_status_entrypoint(DummyRequest())
    print(f"{msg} (HTTP {code})")
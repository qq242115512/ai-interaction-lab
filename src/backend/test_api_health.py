"""最基础的冒烟测试——确保 API 入口能正常返回健康检查。"""
from fastapi.testclient import TestClient


def test_health_endpoint():
    """测试 /api/health 返回 ok"""
    from main import app
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

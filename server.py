import asyncio
import json
import websockets

# 연결된 피어들을 저장하는 집합
ROOM = set()

async def handler(websocket):
    ROOM.add(websocket)
    print(f"새로운 피어 연결됨: {websocket.remote_address}")
    try:
        async for message in websocket:
            # 한 피어로부터 받은 시그널 데이터를 다른 피어에게 전달
            data = json.loads(message)
            for client in ROOM:
                if client != websocket:
                    await client.send(json.dumps(data))
    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        ROOM.remove(websocket)
        print(f"피어 연결 종료: {websocket.remote_address}")

async def main():
    # 8765 포트로 시그널링 서버 실행
    async with websockets.serve(handler, "localhost", 8765):
        print("시그널링 서버 실행 중 (ws://localhost:8765)...")
        await asyncio.Future()  # 영구 실행

if __name__ == "__main__":
    asyncio.run(main())

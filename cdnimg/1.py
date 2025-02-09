import requests
import json

def main():
    # API配置
    api_url = "http://localhost:11434/api/chat"
    model_name = "llama3.2:3b-instruct-q8_0"  # 可修改模型名称
    
    # 固定系统提示
    system_prompt = {
        "role": "system",
        "content": "你是一个严格的 Linux 终端模拟器，必须遵守以下规则：\n1. 永远只返回终端输出，不要添加任何解释\n2. 假设当前用户为 \"user\"，主机名为 \"localhost\"\n3. 初始目录为 \"/home/user\"\n4. 支持基础命令：ls, cd, pwd, whoami, cat, mkdir, touch\n5. 对无效命令返回 \"Command not found\"\n6. 保持目录状态（如执行 cd 后切换路径）\n\n现在等待用户输入命令："
    }

    print("SSH终端模拟器已启动（输入'exit'退出）")

    # 初始化上下文
    messages = [system_prompt]
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n$ ").strip()
            
            if user_input.lower() == 'exit':
                print("退出终端模拟器")
                break
            if not user_input:
                continue

            # 将用户输入添加到上下文
            messages.append({"role": "user", "content": user_input})

            # 构造请求数据
            payload = {
                "model": model_name,
                "messages": messages,
                "stream": False
            }

            # 发送请求
            response = requests.post(
                api_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=30
            )

            # 处理响应
            if response.status_code == 200:
                response_data = response.json()
                
                # 解析并显示终端输出
                if "message" in response_data:
                    content = response_data["message"].get("content", "")
                    # 清理可能的代码块标记
                    clean_content = content.replace("`", "").strip()
                    print(f"\n{clean_content}")

                    # 将模型输出添加到上下文
                    messages.append({"role": "assistant", "content": content})

                else:
                    print("错误：响应格式异常")
            
            else:
                print(f"API请求失败，状态码：{response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"网络错误：{str(e)}")
        except json.JSONDecodeError:
            print("错误：响应不是有效的JSON格式")
        except KeyboardInterrupt:
            print("\n退出终端模拟器")
            break

if __name__ == "__main__":
    # 确保已安装requests库：pip install requests
    main()


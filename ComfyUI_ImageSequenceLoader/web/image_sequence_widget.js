// 文件路径: custom_nodes/ComfyUI_ImageSequenceLoader/web/image_sequence_widget.js

// 确保路径正确导入 ComfyUI 的 App 实例
import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Comfy.ImageSequenceLoader.Display",
    async nodeCreated(node) {
        // 只对你的 ImageSequenceLoader 节点应用此逻辑
        if (node.comfyClass === "ImageSequenceLoader") {
            
            // 1. 创建自定义 Widget
            // 使用一个不可序列化的文本 widget 来显示信息
            const infoWidget = node.addWidget("text", "File Info", "Waiting for execution...", function() {});
            infoWidget.name = "File Info";
            infoWidget.type = "custom_display"; 
            infoWidget.serialize = false; 
            
            // 2. 监听节点执行完成事件
            node.onExecuted = function(data) {
                // 检查是否有 FILENAME 输出
                if (data.results && data.results.FILENAME && data.results.FILENAME.length > 0) {
                    const filename = data.results.FILENAME[0];
                    // 更新 Widget 显示内容
                    infoWidget.value = filename;
                    
                    // 可选：更新节点标题
                    node.title = `🖼️ SEQ: ${filename}`;
                    
                    // 强制刷新节点显示
                    app.graph.setDirtyCanvas(true, true);
                } else {
                    infoWidget.value = "Error or No Images Found";
                }
            };
        }
    },
});

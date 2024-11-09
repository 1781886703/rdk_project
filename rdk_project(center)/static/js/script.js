function openSettings(deviceId) {
    console.log("打开设置框，设备ID: " + deviceId);
}

function updateValue(id) {
    const value = document.getElementById(id).value;
    document.getElementById(id + 'Value').textContent = value;
}

document.getElementById("record_duration").addEventListener("input", updateTotalDuration);
document.getElementById("total_record_count").addEventListener("input", updateTotalDuration);

function updateTotalDuration() {
    const duration = parseInt(document.getElementById("record_duration").value);
    const count = parseInt(document.getElementById("total_record_count").value);
    const totalDuration = duration * count;
    document.getElementById("total_duration").textContent = totalDuration + " min";
    document.getElementById("start_record").disabled = totalDuration === 0;
}

document.getElementById("start_record").addEventListener("click", function () {
    console.log("开始录制");
});

document.getElementById("stop_record").addEventListener("click", function () {
    if (confirm("确认要停止录制吗？")) {
        console.log("录制已停止");
    }
});

// new Vue({
//     el: '#app',
//     data: {
//         devices: [
//             { id: 1, name: '设备1', status: '正常', temperature: 25, image_url: '/media/latest_image.jpg', settings: { warmth: 50, brightness: 50, contrast: 50 } },
//             { id: 2, name: '设备2', status: '正常', temperature: 27, image_url: '/media/camera2.jpg', settings: { warmth: 60, brightness: 40, contrast: 70 } },
//             { id: 3, name: '设备3', status: '异常', temperature: 30, image_url: '/media/camera3.jpg', settings: { warmth: 100, brightness: 45, contrast: 65 } },
//             { id: 4, name: '设备4', status: '正常', temperature: 24, image_url: '/media/camera4.jpg', settings: { warmth: 65, brightness: 55, contrast: 80 } },
//         ],
//         selectedDevice: null,
//         statistics: {
//             redLights: 5,
//             greenLights: 3,
//             electricCars: 7,
//             cars: 10,
//             totalTraffic: 15,
//             startTime: '08:00',
//             endTime: '18:00'
//         },
//         recordingStatus: {
//             recordedTime: 0,
//         },
//         recordingSettings: {
//             segmentTime: 10,
//             totalTime: 120,
//             location: ''
//         },
//         timestamp: Date.now()
//     },
//     mounted() {
//         this.selectedDevice = this.devices[0]; // 默认选择第一个设备
//         setInterval(() => {
//             this.timestamp = Date.now(); // 更新时间戳，确保图片刷新
//         }, 1000);
//     },
//     methods: {
//         selectDevice(device) {
//             this.selectedDevice = device;
//         },
//         startRecording() { /* 启动录制逻辑 */ },
//         pauseRecording() { /* 暂停录制逻辑 */ },
//         stopRecording() { /* 停止录制逻辑 */ }
//     }
// });

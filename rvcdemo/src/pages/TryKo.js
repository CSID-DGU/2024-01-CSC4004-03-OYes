import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const TryKo = () => {
  const [logDisplay, setLogDisplay] = useState(false);
  const [rvcEnabled, setRvcEnabled] = useState(false);
  const [recording, setRecording] = useState(false);
  const [logs, setLogs] = useState([]);
  const [responseUrl, setResponseUrl] = useState("");
  const [responseLog, setResponseLog] = useState("");
  const [model, setModel] = useState("ko-KR-Neural2-A");
  const mediaRecorderRef = useRef([]);
  const audioRef = useRef([]);

  useEffect(() => {
    if (audioRef.current && responseUrl) {
      audioRef.current.src = responseUrl;
      audioRef.current.play().catch(error => console.error('Error playing the audio:', error));
    }
    if (responseLog) {
      setLogs((prevLogs) => [...prevLogs, responseLog]);
    }
  }, [responseUrl, responseLog]);

  const toggleLogDisplay = () => {
    setLogDisplay(!logDisplay);
  };

  const toggleRvc = () => {
    setRvcEnabled(!rvcEnabled);
  };

  const handleRecord = async () => {
    if (recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    } else {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = async (event) => {
        const blob = event.data;
        await handleSubmit(blob);

        setLogs((prevLogs) => [...prevLogs, "음성 파일 저장 성공!"]);
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setRecording(true);
      setLogs((prevLogs) => [...prevLogs, "녹음을 시작합니다."]);
    }
  };

  const handleSubmit = async (blob) => {
    if (!blob) {
      setLogs((prevLogs) => [...prevLogs, "녹음된 파일이 없습니다."]);
      return;
    }

    const formData = new FormData();
    formData.append("model", model);
    formData.append("rvc_enabled", rvcEnabled.toString());
    formData.append('file', blob, 'recording.wav');

    try {
      const apiUrl = process.env.REACT_APP_API_URL;
      console.log(apiUrl);
      const response = await axios.post(`${apiUrl}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });

      setLogs((prevLogs) => [...prevLogs, "파일 전송 성공!"]);
      
      if (response.status === 200) {
        const newResponseUrl = URL.createObjectURL(response.data);
        setResponseUrl(newResponseUrl);
        fetchLogs();
      } 
      else {
        throw new Error("Invalid response status: " + response.status);
      }      
    } 
    catch (error) {
      setLogs((prevLogs) => [...prevLogs, "파일 전송 실패: " + error.message]);
    }
  };


  const fetchLogs = async () => {
    try {
      const logUrl = process.env.REACT_APP_LOG_URL;
      const response = await axios.get(`${logUrl}`);
      if (response.status === 200 && response.data) {
        setResponseLog(response.data);
      }
    } 
    catch (error) {
      setLogs((prevLogs) => [...prevLogs, "로그 정보를 가져오는데 실패했습니다: " + error.message]);
    }
  };

  return (
    <div className="container-fluid d-flex flex-column" style={{ height: '100vh' }}>
      <div className="d-flex flex-grow-1 mt-5 justify-content-center" style={{ gap: '20px' }}>
        {logDisplay && (
          <div className={`card shadow-sm w-25 transition-width`} style={{ height: logDisplay ? '100%' : '0', maxHeight: logDisplay ? 'calc(100vh - 150px)' : '0', overflow: 'hidden' }}>
            <div className="card-body">
              <h5 className="card-title">로그</h5>
              <div className="border rounded p-2" style={{ height: 'calc(100vh - 200px)', overflowY: 'auto' }}>
                {logs.map((log, index) => (
                  <p key={index}>{log}</p>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="card shadow-sm w-50 transition-width" style={{ height: '100%', maxHeight: 'calc(100vh - 150px)' }}>
          <div className="card-body d-flex flex-column" style={{ height: '100%' }}>
            <div className="border rounded flex-grow-1 mb-4 d-flex justify-content-center align-items-center" style={{ aspectRatio: '16 / 9', backgroundColor: '#f8f9fa' }}>
              <audio ref={audioRef} controls style={{ width: '100%', margin: '0 20px' }} />
            </div>

            <div className="mb-3">
              <label htmlFor="model" className="form-label">모델</label>
              <select id="model" name="model" className="form-select" value={model} onChange={e => setModel(e.target.value)}>
                <option value="ko-KR-Neural2-A">ko-KR-Neural2-A (여성1)</option>
                <option value="ko-KR-Neural2-B">ko-KR-Neural2-B (여성2)</option>
                <option value="ko-KR-Neural2-C">ko-KR-Neural2-C (남성1)</option>
                <option value="ko-KR-Wavenet-A">ko-KR-Wavenet-A (여성3)</option>
                <option value="ko-KR-Wavenet-B">ko-KR-Wavenet-B (여성4)</option>
                <option value="ko-KR-Wavenet-C">ko-KR-Wavenet-C (남성2)</option>
                <option value="ko-KR-Wavenet-D">ko-KR-Wavenet-D (남성3)</option>
              </select>
            </div>

            <div className="mb-3">
              <p>정확한 결과를 위해서 <b>자신의 성별에 맞는 모델</b>을 선택해 주세요</p>
            </div>

            <div className="d-flex justify-content-start align-items-center mb-3">
              <div className="d-flex align-items-center me-4">
                <label htmlFor="rvc" className="form-check-label me-2">RVC</label>
                <label className="switch">
                  <input id="rvcEnabled" name="rvcEnabled" type="checkbox" onChange={toggleRvc}/>
                  <span className="slider round"></span>
                </label>
              </div>
              <div className="d-flex align-items-center">
                <label htmlFor="logDisplay" className="form-check-label me-2">로그 보기</label>
                <label className="switch">
                  <input id="logDisplay" name="logDisplay" type="checkbox" onChange={toggleLogDisplay} />
                  <span className="slider round"></span>
                </label>
              </div>
            </div>

            <div className="mb-3">
              <p>RVC - {rvcEnabled ? 'on : 사용자의 목소리와 비슷하게 교정합니다.' : 'off : TTS의 음성으로 교정합니다.'}</p>
              <p>로그 보기 - {logDisplay ? 'on : 로그를 표시합니다.' : 'off : 로그를 표시하지 않습니다.'}</p>
            </div>

            <button className="btn btn-primary mt-auto" onClick={handleRecord} style={{ backgroundColor: recording ? '#FF7C80' : '#4E95D9', height: '50px' }}>
              {recording ? '녹음 종료 후 저장 💾' : '녹음 시작 🎙️'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TryKo;
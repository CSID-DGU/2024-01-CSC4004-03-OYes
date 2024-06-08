import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const TryEn = () => {
  const [logDisplay, setLogDisplay] = useState(false);
  const [rvcEnabled, setRvcEnabled] = useState(false);
  const [recording, setRecording] = useState(false);
  const [logs, setLogs] = useState([]);
  const [responseUrl, setResponseUrl] = useState("");
  const [responseLog, setResponseLog] = useState("");
  const [model, setModel] = useState("haehwan_0");
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

  const formatLog = (log) => {
    return log.split('\n').map((line, index) => (
        <span key={index}>
            {line}
            <br />
        </span>
    ));
  };

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

        setLogs((prevLogs) => [...prevLogs, "Audio file saved successfully!"]);
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
      setRecording(true);
      setLogs((prevLogs) => [...prevLogs, "Recording started."]);
    }
  };

  const handleSubmit = async (blob) => {
    if (!blob) {
      setLogs((prevLogs) => [...prevLogs, "No recorded file available."]);
      return;
    }

    const formData = new FormData();
    formData.append("model", model);
    formData.append("rvc_enabled", rvcEnabled.toString());
    formData.append('file', blob, 'recording.wav');

    try {
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await axios.post(`${apiUrl}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });
      if (response.status === 200) {
        const newResponseUrl = URL.createObjectURL(response.data);
        setResponseUrl(newResponseUrl);
        fetchLogs();
      } 
      else {
        throw new Error("Invalid response status: " + response.status);
      }      
    } catch (error) {
      setLogs((prevLogs) => [...prevLogs, "File upload failed: " + error.message]);
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
              <h5 className="card-title">Logs</h5>
              <div className="border rounded p-2" style={{ height: 'calc(100vh - 200px)', overflowY: 'auto' }}>
                {logs.map((log, index) => (
                  <p key={index}>{formatLog(log)}</p>
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
              <label htmlFor="model" className="form-label">Model</label>
              <select id="model" name="model" className="form-select" value={model} onChange={e => setModel(e.target.value)}>
                <option value="haehwan_0">haehwan_0</option>
                <option value="hong_12">hong_12</option>
                <option value="hyeonmoo_0">hyeonmoo_0</option>
                <option value="IU_12">IU_12</option>
                <option value="jang_0">jang_0</option>
                <option value="sanghyeon_0">sanghyeon_0</option>
                <option value="taeyoung_0">taeyoung_0</option>
                <option value="yonghee_0">yonghee_0</option>
                <option value="yoonyoung_12">yoonyoung_12</option>
              </select>
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
                <label htmlFor="logDisplay" className="form-check-label me-2">show log</label>
                <label className="switch">
                  <input id="logDisplay" name="logDisplay" type="checkbox" onChange={toggleLogDisplay} />
                  <span className="slider round"></span>
                </label>
              </div>
            </div>

            <div className="mb-3">
              <p>RVC - {rvcEnabled ? 'on: Corrects to sound similar to the selected RVC model\'s voice.' : 'off: Corrects to TTS voice.'}</p>
              <p>show log - {logDisplay ? 'on: Shows logs.' : 'off: Does not show logs.'}</p>
            </div>

            <button className="btn btn-primary mt-auto" onClick={handleRecord} style={{ backgroundColor: recording ? '#FF7C80' : '#4E95D9', height: '50px' }}>
              {recording ? 'end recording and save 💾' : 'start recording 🎙️'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TryEn;
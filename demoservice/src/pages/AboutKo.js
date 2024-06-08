import React from 'react';
import structImg from '../images/structKO.png';
import './About.css';

const AboutKo = () => {
  return(
    <div className="container my-5">
      <div className="card">
        <div className="card-body">
          <h1 className="card-title mb-4">Speech Correction with RVC</h1>
          <p className="card-text mb-4">
            Speech Correction with RVC는 생성형 AI와, 화자의 음성의 학습하여 이를 바탕으로 음성을 변환하는 RVC(Retrieval-based Voice Conversion) 기술을 이용하여 한국어 음성에서 의미 전달을 방해하는 요소를 수정하고, 청자가 이질감을 느끼지 않도록 화자의 원래 목소리와 똑같은 교정된 음성을 제공하는 모델입니다.
          </p>
          <h2 className="card-title mb-2">사용법</h2>
          <div className="border p-4 mb-4">
            <table className="table">
              <thead>
                <tr>
                  <th>기능</th>
                  <th>Content-Type</th>
                  <th>메서드</th>
                  <th>요청 URL</th>
                  <th>Request Parameters</th>
                  <th>Response</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>음성 교정</td>
                  <td>multipart/form-data</td>
                  <td>POST</td>
                  <td>http://{'{server_url}'}/speech-correction</td>
                  <td>
                    <ul>
                      <li>model: String, 필수</li>
                      <li>rvc_enabled: Boolean, 필수</li>
                      <li>file: blob, 필수</li>
                    </ul>
                  </td>
                  <td>data: blob, 필수</td>
                </tr>
                <tr>
                  <td>로그 불러오기</td>
                  <td>multipart/form-data</td>
                  <td>GET</td>
                  <td>http://{'{server_url}'}/log</td>
                  <td>없음</td>
                  <td>data: String, 필수</td>
                </tr>
              </tbody>
            </table>
          </div>
          <h2 className="card-title mb-2">구조</h2>
          <div className="border p-4">
            <div className="d-flex justify-content-center">
              <img src={structImg} className="responsiveImage" alt="구조 이미지" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutKo;
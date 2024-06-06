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
            {/* Placeholder for usage instructions */}
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
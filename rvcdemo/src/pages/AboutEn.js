import React from 'react';
import structImg from '../images/structEN.png';
import './About.css';

const AboutEn = () => {
  return(
    <div className="container my-5">
      <div className="card">
        <div className="card-body">
          <h1 className="card-title mb-4">Speech Correction with RVC</h1>
          <p className="card-text mb-4">
            Speech Correction with RVC uses generative AI and the study of the speaker's own voice to transform speech using RVC (Retrieval-based Voice Conversion) technology. This model corrects elements in Korean speech that hinder the transmission of meaning and provides a corrected voice identical to the speaker's original voice, ensuring that listeners do not feel any discomfort.
          </p>
          <h2 className="card-title mb-2">How to use</h2>
          <div className="border p-4 mb-4">
            {/* Placeholder for usage instructions */}
          </div>
          <h2 className="card-title mb-2">Structure</h2>
          <div className="border p-4">
            <div className="d-flex justify-content-center">
              <img src={structImg} className="responsiveImage" alt="struct image" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutEn;
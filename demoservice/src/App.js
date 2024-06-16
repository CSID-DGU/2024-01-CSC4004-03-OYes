import React, {useState} from 'react';
import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import NavBar from './components/NavBar';
import TryKo from './pages/TryKo';
import TryEn from './pages/TryEn';
import AboutKo from './pages/AboutKo';
import AboutEn from './pages/AboutEn';

function App() {
    const [lang, setLang] = useState('ko');

    return (
        <Router>
            <NavBar lang={lang} setLang={setLang}/>
            <Routes>
                <Route path="/try/ko" element={<TryKo/>}/>
                <Route path="/try/en" element={<TryEn/>}/>
                <Route path="/about/ko" element={<AboutKo/>}/>
                <Route path="/about/en" element={<AboutEn/>}/>
                <Route path="*" element={<Navigate to="/try/ko"/>}/>
            </Routes>
        </Router>
    );
}

export default App;
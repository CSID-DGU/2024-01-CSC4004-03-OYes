import React, {useState} from 'react';
import {Link, useLocation, useNavigate} from 'react-router-dom';

const NavBar = ({lang, setLang}) => {
    const location = useLocation();
    const navigate = useNavigate();
    const [langDropdownVisible, setLangDropdownVisible] = useState(false);

    const handleLangChange = (newLang) => {
        setLang(newLang);
        const path = location.pathname.includes('about') ? `/about/${newLang}` : `/try/${newLang}`;
        navigate(path);
        setLangDropdownVisible(false); // 드롭다운 메뉴 숨기기
    };

    const toggleLangDropdown = () => {
        setLangDropdownVisible(!langDropdownVisible);
    };

    return (
        <nav className="navbar navbar-expand navbar-light bg-white shadow-sm">
            <div className="container-fluid">
                <Link to={`/try/${lang}`} className="navbar-brand font-weight-bold">Speech Correction with GPT and RVC</Link>
                <div className="navbar-nav">
                    <Link to={`/try/${lang}`} className="nav-link text-gray-700 me-4">Try</Link>
                    <Link to={`/about/${lang}`} className="nav-link text-gray-700 me-4">About</Link>
                    <div className="nav-item dropdown">
                        <button className="btn btn-link nav-link dropdown-toggle" onClick={toggleLangDropdown}>
                            language
                        </button>
                        <div className={`dropdown-menu dropdown-menu-end ${langDropdownVisible ? 'show' : ''}`}
                             style={{right: 0, left: 'auto'}}>
                            <button className="dropdown-item" onClick={() => handleLangChange('ko')}>
                                <span className="me-2" role="img" aria-label="Korean Flag">🇰🇷</span> 한국어
                            </button>
                            <button className="dropdown-item" onClick={() => handleLangChange('en')}>
                                <span className="me-2" role="img" aria-label="American Flag">🇺🇸</span> English
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;

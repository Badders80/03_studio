import { useState, useRef, useEffect, useLayoutEffect } from 'react';
import { Upload, Download, Sparkles, Image as ImageIcon, Check, Sliders, Layout, Type, Layers } from 'lucide-react';
import html2canvas from 'html2canvas';

// 8 Verified Raw Photographic Assets from Content_Dump
const IMAGE_PRESETS = [
  { id: 'preset_1', name: 'Isolated Portrait (Lucky Strike)', path: '../Content_Dump/492122140801399465.png', desc: 'Ideal for Style 1: Isolated Hero' },
  { id: 'preset_2', name: 'Moody Trackwork (Rider)', path: '../Content_Dump/Screenshot 2026-06-03 152649.png', desc: 'Ideal for Style 2: Moody Noir' },
  { id: 'preset_3', name: 'High-Contrast Gallop', path: '../Content_Dump/6750355478621477852.png', desc: 'High-energy side lit shot' },
  { id: 'preset_4', name: 'Extreme High-Res Stallion', path: '../Content_Dump/16467040852021245604.png', desc: 'Premium micro-texture detail' },
  { id: 'preset_5', name: 'Atmospheric Fog Run', path: '../Content_Dump/16638850641836831858.png', desc: 'Rich depth and moisture texture' },
  { id: 'preset_6', name: 'Sunlit Sunrise Paddock', path: '../Content_Dump/897618565531291341.png', desc: 'Warm amber tones and long shadows' },
  { id: 'preset_7', name: 'Full-Speed Sectional Panning', path: '../Content_Dump/18136941344295886975.png', desc: 'Ideal for Style 4: Telemetry Motion Blur' },
  { id: 'preset_8', name: 'Intimate Detail Closeup', path: '../Content_Dump/12125433371674590499.jpg', desc: 'Shallow DOF, ideal for Style 3' },
  { id: 'preset_9', name: 'Prudentia Action Gallop', path: '../Content_Dump/prudentia_action_shot.png', desc: 'Classic racecourse finish photo' }
];

// Custom Signature SVGs
const SIGNATURE_PRESETS = [
  { id: 'none', name: 'Classic Editorial Serif' },
  { id: 'script', name: 'Elegant Handwriting Font' },
  { id: 'prudentia', name: 'Prudentia Hand-Signature (SVG)', path: '../Content_Dump/Prudentia_Logo (2).svg' },
  { id: 'hottathen', name: 'Hottathen Hand-Signature (SVG)', path: '../Content_Dump/Hottathen_Logo.svg' }
];

export default function App() {
  // 1. Photographic States
  const [selectedPreset, setSelectedPreset] = useState(IMAGE_PRESETS[0].id);
  const [imageSrc, setImageSrc] = useState(IMAGE_PRESETS[0].path);
  const [imageName, setImageName] = useState(IMAGE_PRESETS[0].name);
  const [imageScale, setImageScale] = useState(1.15);
  const [imageFocusX, setImageFocusX] = useState(50);
  const [imageFocusY, setImageFocusY] = useState(50);

  // 2. Poster Style Grade States
  const [posterStyle, setPosterStyle] = useState('isolated'); // isolated, moody, editorial, telemetry
  const [composition, setComposition] = useState('bottom'); // left, right, top, bottom

  // 3. Editorial & Typography States
  const [contextTag, setContextTag] = useState('NEXT UP | EVOLUTION');
  const [heroTitle, setHeroTitle] = useState('Lucky Strike');
  const [signatureStyle, setSignatureStyle] = useState('none'); // none, script, prudentia, hottathen
  const [sparkGold, setSparkGold] = useState(false);
  const [goldIntensity, setGoldIntensity] = useState(100);

  // 4. Overlay Widget States
  const [overlayMode, setOverlayMode] = useState('telemetry'); // telemetry, quote, glasscard, none

  // Telemetry Bar States
  const [telCol1Val, setTelCol1Val] = useState('15 MAR');
  const [telCol1Label, setTelCol1Label] = useState('DATE');
  const [telCol2Val, setTelCol2Val] = useState('1ST PLACE');
  const [telCol2Label, setTelCol2Label] = useState('RESULT');
  const [telCol3Val, setTelCol3Val] = useState('1:10.24');
  const [telCol3Label, setTelCol3Label] = useState('TIME');

  // Quote States
  const [quoteText, setQuoteText] = useState('He was traveling beautifully on the corner and let down with immense acceleration when balanced.');
  const [quoteAttribution, setQuoteAttribution] = useState('— MASA HASHIZUME | JOCKEY');

  // Glass Card States
  const [cardHeader, setCardCardHeader] = useState('LUCKY STRIKE');
  const [cardStatus, setCardStatus] = useState('BACK IN TRAINING');
  const [cardDesc, setCardDesc] = useState('Completing quiet pacework over 800m. Retaining high level of fitness.');

  // Branding States
  const [monogramOpacity, setMonogramOpacity] = useState(30);

  // System States
  const [isExporting, setIsExporting] = useState(false);
  const [scaleFactor, setScaleFactor] = useState(0.5);
  const workspaceRef = useRef(null);

  // Auto-scale workspace poster preview to fit user screen
  useEffect(() => {
    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        const { width, height } = entry.contentRect;
        const scaleW = (width - 60) / 1080;
        const scaleH = (height - 60) / 1350;
        setScaleFactor(Math.min(scaleW, scaleH, 0.9));
      }
    });

    if (workspaceRef.current) {
      resizeObserver.observe(workspaceRef.current);
    }
    return () => resizeObserver.disconnect();
  }, []);

  // Preset Selection Handler
  const handlePresetChange = (id) => {
    setSelectedPreset(id);
    const preset = IMAGE_PRESETS.find(p => p.id === id);
    if (preset) {
      setImageSrc(preset.path);
      setImageName(preset.name);
      
      // Auto-configure optimal visual pairing defaults based on selected preset
      if (id === 'preset_1' || id === 'preset_4') {
        setPosterStyle('isolated');
        setComposition('bottom');
      } else if (id === 'preset_2' || id === 'preset_5') {
        setPosterStyle('moody');
        setComposition('left');
      } else if (id === 'preset_7') {
        setPosterStyle('telemetry');
        setComposition('bottom');
      } else if (id === 'preset_8') {
        setPosterStyle('editorial');
        setComposition('right');
      }
    }
  };

  // Image Upload handler
  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedPreset('custom');
      setImageName(file.name);
      const reader = new FileReader();
      reader.onload = (event) => {
        setImageSrc(event.target?.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Format Context Tag (Clean separating pipes)
  const getDisplayContextTag = () => {
    const trimmed = contextTag.trim();
    if (trimmed === '') return '...';
    // Clean any colons and enforce the clean technical separator pipe '|'
    return trimmed.replace(/:/g, '|').toUpperCase();
  };

  // Export High-Res PNG via html2canvas (forced Scale: 2 for print-ready 2160x2700 result)
  const handleExport = async () => {
    const canvasElement = document.getElementById('poster-render-target');
    if (!canvasElement || isExporting) return;

    setIsExporting(true);
    try {
      const canvas = await html2canvas(canvasElement, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#000000',
        width: 1080,
        height: 1350,
        logging: false
      });

      canvas.toBlob((blob) => {
        if (blob) {
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          const fileName = heroTitle.trim().replace(/\s+/g, '-').toLowerCase() || 'poster';
          a.download = `evolution-${fileName}-poster.png`;
          a.click();
          URL.revokeObjectURL(url);
        }
        setIsExporting(false);
      }, 'image/png');
    } catch (err) {
      console.error('Failed to export canvas:', err);
      setIsExporting(false);
    }
  };

  return (
    <div className="app-container">
      {/* SIDEBAR CONTROL DASHBOARD */}
      <aside className="control-panel">
        <div className="panel-header">
          <h1 className="logo-text">EVOLUTION <span>STUDIO</span></h1>
          <p className="panel-subtitle">UI/UX Pro Max Poster & Social Engine</p>
        </div>

        <div className="form-content">
          {/* Z-1: BACKGROUND PHOTO & LENS SELECTOR */}
          <div className="control-card">
            <h2 className="card-title">
              <ImageIcon size={14} className="title-icon" />
              Z-1: Action Lens
            </h2>
            
            <div className="form-group">
              <label>Select Raw Horse Asset</label>
              <select 
                value={selectedPreset} 
                onChange={(e) => handlePresetChange(e.target.value)}
                className="preset-select"
              >
                {IMAGE_PRESETS.map((preset) => (
                  <option key={preset.id} value={preset.id}>
                    {preset.name}
                  </option>
                ))}
                <option value="custom">[Custom Uploaded Photo]</option>
              </select>
            </div>

            <div className="form-group">
              <label>Or Upload Custom Photo</label>
              <label className="file-upload-btn">
                <Upload size={14} />
                Upload File
                <input 
                  type="file" 
                  accept="image/*" 
                  onChange={handleImageUpload} 
                  style={{ display: 'none' }} 
                />
              </label>
              {selectedPreset === 'custom' && <p className="file-name-preview">{imageName}</p>}
            </div>

            <div className="input-row">
              <div className="form-group">
                <div className="slider-val-row">
                  <label>Scale</label>
                  <span className="slider-val">{imageScale.toFixed(2)}x</span>
                </div>
                <input 
                  type="range" 
                  min="0.5" 
                  max="3" 
                  step="0.05"
                  value={imageScale} 
                  onChange={(e) => setImageScale(parseFloat(e.target.value))} 
                />
              </div>

              <div className="form-group">
                <div className="slider-val-row">
                  <label>Monogram</label>
                  <span className="slider-val">{monogramOpacity}%</span>
                </div>
                <input 
                  type="range" 
                  min="0" 
                  max="100" 
                  step="5"
                  value={monogramOpacity} 
                  onChange={(e) => setMonogramOpacity(parseInt(e.target.value))} 
                />
              </div>
            </div>

            <div className="input-row">
              <div className="form-group">
                <div className="slider-val-row">
                  <label>Focus X</label>
                  <span className="slider-val">{imageFocusX}%</span>
                </div>
                <input 
                  type="range" 
                  min="0" 
                  max="100" 
                  value={imageFocusX} 
                  onChange={(e) => setImageFocusX(parseInt(e.target.value))} 
                />
              </div>

              <div className="form-group">
                <div className="slider-val-row">
                  <label>Focus Y</label>
                  <span className="slider-val">{imageFocusY}%</span>
                </div>
                <input 
                  type="range" 
                  min="0" 
                  max="100" 
                  value={imageFocusY} 
                  onChange={(e) => setImageFocusY(parseInt(e.target.value))} 
                />
              </div>
            </div>
          </div>

          {/* STYLE GRADE & COMPOSITION MAP */}
          <div className="control-card">
            <h2 className="card-title">
              <Sliders size={14} className="title-icon" />
              Z-2: Aesthetic & Composition
            </h2>

            <div className="form-group">
              <label>Photographic Style Grade</label>
              <div className="style-grid-selector">
                <button 
                  className={`style-btn ${posterStyle === 'isolated' ? 'active' : ''}`}
                  onClick={() => setPosterStyle('isolated')}
                >
                  Isolated Hero
                  <span>Solid black backdrop</span>
                </button>
                <button 
                  className={`style-btn ${posterStyle === 'moody' ? 'active' : ''}`}
                  onClick={() => setPosterStyle('moody')}
                >
                  Moody Noir
                  <span>Dark vignette & film grain</span>
                </button>
                <button 
                  className={`style-btn ${posterStyle === 'editorial' ? 'active' : ''}`}
                  onClick={() => setPosterStyle('editorial')}
                >
                  Editorial Warm
                  <span>Golden hour shallow bokeh</span>
                </button>
                <button 
                  className={`style-btn ${posterStyle === 'telemetry' ? 'active' : ''}`}
                  onClick={() => setPosterStyle('telemetry')}
                >
                  Kinetic Speed
                  <span>Overcast motion vignette</span>
                </button>
              </div>
            </div>

            <div className="form-group">
              <label>Composition Empty Space (Layout Anchor)</label>
              <div className="layout-quad-selector">
                <button 
                  className={`quad-btn ${composition === 'left' ? 'active' : ''}`}
                  onClick={() => setComposition('left')}
                  title="Photo is on right, overlay sits Left"
                >
                  Left Empty
                </button>
                <button 
                  className={`quad-btn ${composition === 'right' ? 'active' : ''}`}
                  onClick={() => setComposition('right')}
                  title="Photo is on left, overlay sits Right"
                >
                  Right Empty
                </button>
                <button 
                  className={`quad-btn ${composition === 'top' ? 'active' : ''}`}
                  onClick={() => setComposition('top')}
                  title="Photo is at bottom, overlay sits Top"
                >
                  Top Empty
                </button>
                <button 
                  className={`quad-btn ${composition === 'bottom' ? 'active' : ''}`}
                  onClick={() => setComposition('bottom')}
                  title="Photo is at top, overlay sits Bottom"
                >
                  Bottom Empty
                </button>
              </div>
              <p className="helper-text-small">
                {composition === 'left' && "Aligns and stacks text completely Left within negative space."}
                {composition === 'right' && "Aligns and stacks text completely Right within negative space."}
                {composition === 'top' && "Places brand assets and overlays neatly at the top."}
                {composition === 'bottom' && "Standard editorial grid spanning the bottom third."}
              </p>
            </div>
          </div>

          {/* EDITORIAL CONTENT & TYPOGRAPHY */}
          <div className="control-card">
            <h2 className="card-title">
              <Type size={14} className="title-icon" />
              Z-3 & Z-4: Identity & Typography
            </h2>

            <div className="form-group">
              <label>Context Header Tag</label>
              <input 
                type="text" 
                value={contextTag} 
                onChange={(e) => setContextTag(e.target.value)} 
                placeholder="e.g. NEXT UP | EVOLUTION"
              />
            </div>

            <div className="form-group">
              <label>Horse Name (Main Subject Title)</label>
              <input 
                type="text" 
                value={heroTitle} 
                onChange={(e) => setHeroTitle(e.target.value)} 
                placeholder="e.g. Lucky Strike"
              />
            </div>

            <div className="form-group">
              <label>Typography Name Style</label>
              <select 
                value={signatureStyle} 
                onChange={(e) => setSignatureStyle(e.target.value)}
                className="preset-select"
              >
                {SIGNATURE_PRESETS.map((style) => (
                  <option key={style.id} value={style.id}>
                    {style.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input 
                  type="checkbox" 
                  checked={sparkGold} 
                  onChange={(e) => setSparkGold(e.target.checked)} 
                />
                Use Gold Sparing Accent (#D4A964)
              </label>
              {sparkGold && (
                <div className="slider-val-row" style={{ marginTop: '4px' }}>
                  <label>Gold Hue Pop</label>
                  <input 
                    type="range" 
                    min="50" 
                    max="100" 
                    value={goldIntensity} 
                    onChange={(e) => setGoldIntensity(parseInt(e.target.value))} 
                    style={{ width: '120px' }}
                  />
                </div>
              )}
            </div>
          </div>

          {/* LAYOUT WIDGETS */}
          <div className="control-card">
            <h2 className="card-title">
              <Layers size={14} className="title-icon" />
              Z-5: Content Overlay Widget
            </h2>

            <div className="form-group">
              <label>Widget Overlay Mode</label>
              <div className="widget-toggle-row">
                <button 
                  className={`widget-btn ${overlayMode === 'telemetry' ? 'active' : ''}`}
                  onClick={() => setOverlayMode('telemetry')}
                >
                  Telemetry
                </button>
                <button 
                  className={`widget-btn ${overlayMode === 'quote' ? 'active' : ''}`}
                  onClick={() => setOverlayMode('quote')}
                >
                  Quote
                </button>
                <button 
                  className={`widget-btn ${overlayMode === 'glasscard' ? 'active' : ''}`}
                  onClick={() => setOverlayMode('glasscard')}
                >
                  Glass Card
                </button>
                <button 
                  className={`widget-btn ${overlayMode === 'none' ? 'active' : ''}`}
                  onClick={() => setOverlayMode('none')}
                >
                  None
                </button>
              </div>
            </div>

            {/* Telemetry Form Fields */}
            {overlayMode === 'telemetry' && (
              <div className="widget-inputs-container">
                <div className="nested-input-row">
                  <div className="form-group">
                    <label>Col 1 Val</label>
                    <input type="text" value={telCol1Val} onChange={(e) => setTelCol1Val(e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label>Label</label>
                    <input type="text" value={telCol1Label} onChange={(e) => setTelCol1Label(e.target.value)} />
                  </div>
                </div>
                <div className="nested-input-row">
                  <div className="form-group">
                    <label>Col 2 Val</label>
                    <input type="text" value={telCol2Val} onChange={(e) => setTelCol2Val(e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label>Label</label>
                    <input type="text" value={telCol2Label} onChange={(e) => setTelCol2Label(e.target.value)} />
                  </div>
                </div>
                <div className="nested-input-row">
                  <div className="form-group">
                    <label>Col 3 Val</label>
                    <input type="text" value={telCol3Val} onChange={(e) => setTelCol3Val(e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label>Label</label>
                    <input type="text" value={telCol3Label} onChange={(e) => setTelCol3Label(e.target.value)} />
                  </div>
                </div>
              </div>
            )}

            {/* Quote Form Fields */}
            {overlayMode === 'quote' && (
              <div className="widget-inputs-container">
                <div className="form-group">
                  <label>Trainer/Jockey Quote (No marks)</label>
                  <textarea 
                    value={quoteText} 
                    onChange={(e) => setQuoteText(e.target.value)} 
                    rows={3}
                    className="widget-textarea"
                  />
                </div>
                <div className="form-group">
                  <label>Attribution (Use clean | separators)</label>
                  <input type="text" value={quoteAttribution} onChange={(e) => setQuoteAttribution(e.target.value)} />
                </div>
              </div>
            )}

            {/* Glass Card Form Fields */}
            {overlayMode === 'glasscard' && (
              <div className="widget-inputs-container">
                <div className="form-group">
                  <label>Card Title Header</label>
                  <input type="text" value={cardHeader} onChange={(e) => setCardCardHeader(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Status Action Tag</label>
                  <input type="text" value={cardStatus} onChange={(e) => setCardStatus(e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Card Status Description</label>
                  <textarea 
                    value={cardDesc} 
                    onChange={(e) => setCardDesc(e.target.value)} 
                    rows={2}
                    className="widget-textarea"
                  />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* BOTTOM EXPORT ROW */}
        <div className="action-row">
          <button 
            className="btn-primary" 
            onClick={handleExport}
            disabled={isExporting}
          >
            {isExporting ? (
              <>
                <Sparkles size={18} className="spinning" />
                Rendering Print File...
              </>
            ) : (
              <>
                <Download size={18} />
                Export 2x DPI Poster PNG
              </>
            )}
          </button>
        </div>
      </aside>

      {/* RIGHT PREVIEW WORKSPACE */}
      <section className="preview-workspace" ref={workspaceRef}>
        <div 
          className="canvas-wrapper"
          style={{
            transform: `scale(${scaleFactor})`,
            width: 1080,
            height: 1350
          }}
        >
          {/* THE 1080x1350 POSTER RENDER TARGET */}
          <div 
            className={`poster-canvas style-grade-${posterStyle} composition-${composition}`} 
            id="poster-render-target"
          >
            {/* Z-0 Stack: Film Grain overlay layer */}
            <div className="grain-layer"></div>

            {/* Photographic Color-grading Overlays based on chosen Style */}
            <div className={`filter-overlay grade-${posterStyle}`}></div>
            <div className={`vignette-overlay grade-${posterStyle}`}></div>

            {/* Z-1: Action Lens Image Frame */}
            <div className="action-lens-wrapper">
              {imageSrc ? (
                <img 
                  src={imageSrc} 
                  alt="Action Lens Shot" 
                  className="action-lens-image"
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    transform: `translate(-50%, -50%) scale(${imageScale})`,
                    left: `${imageFocusX}%`,
                    top: `${imageFocusY}%`
                  }}
                />
              ) : (
                <div className="no-image-wrapper">
                  <ImageIcon size={64} style={{ marginBottom: '12px', color: '#444' }} />
                  <p>No Action Lens Photo Loaded</p>
                </div>
              )}
            </div>

            {/* ========================================================================= */}
            {/* COMPOSITION-AWARE LAYOUT WRAPPER                                         */}
            {/* Dynamically shifts alignment & order based on negative space requirements */}
            {/* ========================================================================= */}
            <div className={`layout-overlay-container align-${composition}`}>
              
              {/* Context Tag Header */}
              <div className="context-tag">
                {getDisplayContextTag()}
              </div>

              {/* Horse Identity / Signature Title */}
              <div className="hero-identity-block">
                {signatureStyle === 'none' ? (
                  <h1 className={`hero-title-editorial ${sparkGold ? 'gold-glow' : ''}`}>
                    {heroTitle}
                  </h1>
                ) : signatureStyle === 'script' ? (
                  <h1 className={`hero-title-script ${sparkGold ? 'gold-glow' : ''}`}>
                    {heroTitle}
                  </h1>
                ) : signatureStyle === 'prudentia' ? (
                  <div className="signature-svg-wrapper">
                    <img 
                      src="../Content_Dump/Prudentia_Logo (2).svg" 
                      alt="Prudentia Signature" 
                      className={`signature-svg-img ${sparkGold ? 'gold-color' : 'white-color'}`}
                      style={{
                        filter: sparkGold ? `sepia(0.3) saturate(1.5) hue-rotate(-10deg) brightness(${goldIntensity / 100})` : 'brightness(1.5) contrast(2)'
                      }}
                    />
                  </div>
                ) : signatureStyle === 'hottathen' ? (
                  <div className="signature-svg-wrapper">
                    <img 
                      src="../Content_Dump/Hottathen_Logo.svg" 
                      alt="Hottathen Signature" 
                      className={`signature-svg-img ${sparkGold ? 'gold-color' : 'white-color'}`}
                      style={{
                        filter: sparkGold ? `sepia(0.3) saturate(1.5) hue-rotate(-10deg) brightness(${goldIntensity / 100})` : 'brightness(1.5) contrast(2)'
                      }}
                    />
                  </div>
                ) : null}
              </div>

              {/* Dynamic Overlay Widgets */}
              {overlayMode !== 'none' && (
                <div className="dynamic-widget-area">
                  
                  {/* Telemetry Bar Widget */}
                  {overlayMode === 'telemetry' && (
                    <div className="telemetry-bar">
                      <div className="telemetry-col">
                        <div className="tel-val">{telCol1Val}</div>
                        <div className="tel-label">{telCol1Label}</div>
                      </div>
                      <div className="telemetry-col">
                        <div className="tel-val">{telCol2Val}</div>
                        <div className="tel-label">{telCol2Label}</div>
                      </div>
                      <div className="telemetry-col">
                        <div className="tel-val">{telCol3Val}</div>
                        <div className="tel-label">{telCol3Label}</div>
                      </div>
                    </div>
                  )}

                  {/* Minimalist Quote Block Widget (No quotation marks, uses clean thin vertical bar) */}
                  {overlayMode === 'quote' && (
                    <div className="quote-block">
                      <div className="quote-accent-bar"></div>
                      <div className="quote-content-wrapper">
                        <blockquote className="quote-text">
                          {quoteText}
                        </blockquote>
                        <cite className="quote-attribution">
                          {quoteAttribution.replace(/:/g, '|').toUpperCase()}
                        </cite>
                      </div>
                    </div>
                  )}

                  {/* Segmented Glass Card Widget */}
                  {overlayMode === 'glasscard' && (
                    <div className="segmented-glass-card">
                      <div className="card-top">
                        <div className="card-title-header">{cardHeader}</div>
                        <div className={`card-status-pill ${sparkGold ? 'gold-accent' : ''}`}>
                          {cardStatus}
                        </div>
                      </div>
                      <div className="card-bottom">
                        <p className="card-desc">{cardDesc}</p>
                      </div>
                    </div>
                  )}

                </div>
              )}
            </div>

            {/* Z-6: Brand Monogram Watermark */}
            <div 
              className={`brand-watermark position-${composition}`}
              style={{ opacity: monogramOpacity / 100 }}
            >
              <svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" viewBox="-10.00 -10.00 127.78 114.41" width="120" height="108">
                <path d="M85.38,15.12c-1.96-2.03-4.1-3.89-6.38-5.55h0c-.87-.64-1.83-1.28-2.91-1.96h0C68.13,2.63,58.94,0,49.51,0,22.21,0,0,21.82,0,48.64c0,19.79,12.04,37.46,30.68,44.99,0,0,1.47,.59,2.37,.78l14.15-24.51,19.8,17.29L107.78,15.12h-22.4Zm-7.62,29.2l-13.67,24.16-11.69-9.3,5.72-10.28,2.43,1.12c-2.25-3.1-4.71-9.52-4.73-13.31l-25.3,43.82c-11.55-6.55-18.77-18.59-18.77-31.9-.01-20.33,16.93-36.89,37.76-36.89,7.23,0,14.26,2.01,20.34,5.82,.85,.53,1.58,1.02,2.23,1.5h0c2.31,1.68,4.42,3.63,6.28,5.78l1.76,2.03h14.26l-12.13,9.55-4.48,7.92v-.02Z" />
              </svg>
            </div>

            {/* Safe zone boundary guide */}
            <div className="padding-guide"></div>

          </div>
        </div>
      </section>
    </div>
  );
}

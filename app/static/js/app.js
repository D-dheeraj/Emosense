// Production Application Controller for EmoSense
class EmoSenseApp {
  constructor() {
    this.video = document.getElementById('webcamVideo');
    this.canvas = document.getElementById('canvasOverlay');
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;

    this.selectedEmoji = '😀';
    this.selectedMood = 'Happy';
    this.currentBase64Frame = null;
    this.frameAnalysisTimer = null;

    this.initTabs();
    this.initEmojiPicker();
    this.initWebcam();
    this.initCheckInButton();
    this.initChatbotWidget();
    this.initAudioPlayer();
    this.loadHistory();
  }

  // 1. Navigation Tab Switcher
  initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');

        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        const contentEl = document.getElementById(targetTab);
        if (contentEl) contentEl.classList.add('active');
      });
    });
  }

  // 2. Emoji Mood Grid Picker
  initEmojiPicker() {
    const buttons = document.querySelectorAll('.emoji-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.selectedEmoji = btn.getAttribute('data-emoji');
        this.selectedMood = btn.getAttribute('data-mood');
      });
    });
  }

  // 3. Initialize Webcam Stream
  async initWebcam() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      const tag = document.getElementById('liveEmotionTag');
      if (tag) tag.textContent = 'Camera Unavailable';
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' }
      });
      this.video.srcObject = stream;

      this.video.onloadedmetadata = () => {
        this.canvas.width = this.video.videoWidth || 640;
        this.canvas.height = this.video.videoHeight || 480;
        this.startRealtimeFrameLoop();
      };
    } catch (err) {
      console.warn('Webcam permission error:', err);
      const tag = document.getElementById('liveEmotionTag');
      if (tag) tag.textContent = 'Camera Off (Snapshot Fallback)';
    }
  }

  // 4. Real-time Edge AI Frame Evaluation (600ms)
  startRealtimeFrameLoop() {
    if (this.frameAnalysisTimer) clearInterval(this.frameAnalysisTimer);

    this.frameAnalysisTimer = setInterval(async () => {
      if (!this.video || this.video.paused || this.video.ended) return;

      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = this.video.videoWidth || 640;
      tempCanvas.height = this.video.videoHeight || 480;
      const tempCtx = tempCanvas.getContext('2d');
      tempCtx.drawImage(this.video, 0, 0, tempCanvas.width, tempCanvas.height);

      const base64Img = tempCanvas.toDataURL('image/jpeg', 0.8);
      this.currentBase64Frame = base64Img;

      try {
        const response = await fetch('/api/analyze-frame', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_base64: base64Img })
        });
        const data = await response.json();
        this.renderFrameAnalysisResult(data);
      } catch (err) {
        // Silent catch for live stream
      }
    }, 600);
  }

  renderFrameAnalysisResult(data) {
    if (!this.ctx) return;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    const emotionTag = document.getElementById('liveEmotionTag');
    const confBar = document.getElementById('confidenceBar');

    if (data.face_detected && data.bounding_box) {
      const { x, y, w, h } = data.bounding_box;

      this.ctx.strokeStyle = '#00f2fe';
      this.ctx.lineWidth = 3;
      this.ctx.shadowColor = '#00f2fe';
      this.ctx.shadowBlur = 15;
      this.ctx.strokeRect(x, y, w, h);
      this.ctx.shadowBlur = 0;

      this.ctx.fillStyle = 'rgba(0, 242, 254, 0.85)';
      this.ctx.fillRect(x, Math.max(0, y - 28), w, 26);
      this.ctx.fillStyle = '#070913';
      this.ctx.font = 'bold 14px Outfit';
      this.ctx.fillText(`${data.dominant_emotion} (${Math.round(data.confidence * 100)}%)`, x + 8, Math.max(18, y - 10));

      if (emotionTag) emotionTag.textContent = `Visual: ${data.dominant_emotion}`;
      if (confBar) confBar.style.width = `${Math.round(data.confidence * 100)}%`;
    } else {
      if (emotionTag) emotionTag.textContent = `Visual: Neutral`;
      if (confBar) confBar.style.width = `50%`;
    }
  }

  // 5. Submit 3-Way Congruence Check-in
  initCheckInButton() {
    const btn = document.getElementById('analyzeBtn');
    if (!btn) return;

    btn.addEventListener('click', async () => {
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Triangulating Signals via Gemini Agent...</span>';

      const journalText = document.getElementById('journalInput').value.trim();

      const payload = {
        image_base64: this.currentBase64Frame,
        journal_text: journalText,
        self_reported_emoji: this.selectedEmoji,
        self_reported_mood: this.selectedMood
      };

      try {
        const response = await fetch('/api/checkin', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const result = await response.json();
        this.updateDashboardResults(result);
        this.loadHistory();
      } catch (err) {
        alert('Check-in evaluation failed. Please check network connection.');
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> <span>Run 3-Way Congruence Check-In</span>';
      }
    });
  }

  updateDashboardResults(data) {
    const gaugeValue = document.getElementById('congruenceValue');
    const gaugeCircle = document.getElementById('congruenceGauge');
    if (gaugeValue) gaugeValue.textContent = `${Math.round(data.congruence_score)}%`;
    if (gaugeCircle) {
      const deg = Math.round((data.congruence_score / 100) * 360);
      const color = data.is_emotional_masking ? '#f43f5e' : (data.congruence_score < 70 ? '#f59e0b' : '#00f2fe');
      gaugeCircle.style.background = `conic-gradient(${color} 0deg ${deg}deg, rgba(255,255,255,0.1) ${deg}deg 360deg)`;
    }

    const alertBanner = document.getElementById('maskingAlertBanner');
    const alertIcon = document.getElementById('alertIcon');
    const alertExp = document.getElementById('alertExplanation');
    const badge = document.getElementById('maskingStatusBadge');

    if (alertBanner && alertExp) {
      if (data.is_emotional_masking) {
        alertBanner.className = 'masking-alert-banner masking';
        if (alertIcon) alertIcon.className = 'fa-solid fa-triangle-exclamation';
        alertExp.textContent = `EMOTIONAL MASKING DETECTED: Visual expression (${data.visual_emotion}) masks distress in journal text.`;
        if (badge) {
          badge.textContent = 'Masked Distress Alert!';
          badge.style.background = 'rgba(244,63,94,0.2)';
          badge.style.color = '#f43f5e';
        }
      } else if (data.congruence_score < 75) {
        alertBanner.className = 'masking-alert-banner discrepancy';
        if (alertIcon) alertIcon.className = 'fa-solid fa-circle-exclamation';
        alertExp.textContent = `MILD DISCREPANCY: Slight variation observed between visual expression and text sentiment.`;
        if (badge) {
          badge.textContent = 'Mild Discrepancy';
          badge.style.background = 'rgba(245,158,11,0.2)';
          badge.style.color = '#f59e0b';
        }
      } else {
        alertBanner.className = 'masking-alert-banner congruent';
        if (alertIcon) alertIcon.className = 'fa-solid fa-circle-check';
        alertExp.textContent = `CONGRUENT SIGNALS: Visual expression (${data.visual_emotion}), text tone, and emoji mood are well aligned.`;
        if (badge) {
          badge.textContent = 'High Congruence';
          badge.style.background = 'rgba(16,185,129,0.2)';
          badge.style.color = '#10b981';
        }
      }
    }

    const summaryText = document.getElementById('wellnessSummaryText');
    const interventionTag = document.getElementById('recommendedInterventionTag');

    if (summaryText) summaryText.textContent = data.wellness_summary;
    if (interventionTag) interventionTag.textContent = data.recommended_intervention;
  }

  // 6. Floating AI Assistant Chatbot Drawer Handler
  initChatbotWidget() {
    const toggleBtn = document.getElementById('chatToggleBtn');
    const drawer = document.getElementById('chatDrawer');
    const closeBtn = document.getElementById('chatCloseBtn');
    const sendBtn = document.getElementById('chatSendBtn');
    const chatInput = document.getElementById('chatInput');
    const msgContainer = document.getElementById('chatMessages');

    if (!toggleBtn || !drawer) return;

    toggleBtn.addEventListener('click', () => {
      drawer.classList.toggle('open');
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', () => drawer.classList.remove('open'));
    }

    const handleSend = async () => {
      const msg = chatInput.value.trim();
      if (!msg) return;

      this.appendChatMessage('user', msg);
      chatInput.value = '';

      const typingId = this.appendChatMessage('bot', 'AI Assistant is thinking...');

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg })
        });
        const data = await response.json();
        
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.innerHTML = data.reply.replace(/\n/g, '<br/>');
      } catch (err) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) typingEl.textContent = "I'm having trouble connecting right now. Please check your network.";
      }
    };

    if (sendBtn) sendBtn.addEventListener('click', handleSend);
    if (chatInput) {
      chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
      });
    }
  }

  appendChatMessage(sender, text) {
    const msgContainer = document.getElementById('chatMessages');
    if (!msgContainer) return;

    const div = document.createElement('div');
    const id = 'msg-' + Date.now();
    div.id = id;
    div.className = `chat-msg ${sender}`;
    div.innerHTML = text.replace(/\n/g, '<br/>');
    msgContainer.appendChild(div);
    msgContainer.scrollTop = msgContainer.scrollHeight;
    return id;
  }

  // 7. Ambient Audio Soundscape Player Controls
  initAudioPlayer() {
    const playBtn = document.getElementById('audioPlayBtn');
    if (!playBtn) return;

    let isPlaying = false;
    let audioCtx = null;
    let oscillator = null;

    playBtn.addEventListener('click', () => {
      if (isPlaying) {
        isPlaying = false;
        playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
        if (oscillator) oscillator.stop();
      } else {
        isPlaying = true;
        playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
        
        // Web Audio API Ambient Binaural Harmonic Generator for relaxation
        try {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
          oscillator = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          
          oscillator.type = 'sine';
          oscillator.frequency.setValueAtTime(432, audioCtx.currentTime); // 432Hz calming frequency
          gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
          
          oscillator.connect(gain);
          gain.connect(audioCtx.destination);
          oscillator.start();
        } catch (e) {
          console.warn('Web Audio API not supported:', e);
        }
      }
    });
  }

  // 8. Load History
  async loadHistory() {
    try {
      const response = await fetch('/api/history');
      const history = await response.json();
      if (typeof updateTrendChart === 'function') {
        updateTrendChart(history);
      }
    } catch (err) {
      console.warn('Failed to load history trends:', err);
    }
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.emoSenseApp = new EmoSenseApp();
});

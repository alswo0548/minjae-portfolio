'use strict';
// Start the lead clip immediately; load later clips near the viewport.
// Animated WebP fallback never requires clicking to begin playback.
document.querySelectorAll('.media').forEach(stage=>{
 const video=stage.querySelector('video'),status=stage.querySelector('.play-status');
 const pause=stage.querySelector('.pause'),expand=stage.querySelector('.expand');
 let started=false,fallback=false,userPaused=false;
 const useFallback=()=>{
  if(fallback||userPaused)return;
  fallback=true;video.pause();video.hidden=true;
  const img=new Image();img.className='fallback';img.alt=video.getAttribute('aria-label');
  img.onload=()=>{status.textContent='자동 반복 재생 · 애니메이션';};
  img.onerror=()=>{status.textContent='네트워크 오류 · 페이지를 새로고침해 주세요';};
  img.src=video.dataset.fallback;stage.prepend(img);pause.hidden=true;
 };
 const start=()=>{
  if(started)return;started=true;
  video.muted=true;video.defaultMuted=true;
  if(video.dataset.src)video.src=video.dataset.src;
  const promise=video.play();if(promise)promise.catch(useFallback);
 };
 video.addEventListener('playing',()=>{status.textContent='자동 반복 재생 · 실제 녹화';pause.textContent='일시정지';});
 video.addEventListener('waiting',()=>{status.textContent='시연 불러오는 중…';});
 video.addEventListener('error',useFallback);
 pause.addEventListener('click',()=>{
  if(video.paused){userPaused=false;video.play().catch(useFallback);}else{userPaused=true;video.pause();pause.textContent='계속 재생';status.textContent='일시정지';}
 });
 expand.addEventListener('click',()=>{
  if(document.fullscreenElement){document.exitFullscreen();return;}
  if(stage.requestFullscreen)stage.requestFullscreen().catch(()=>{if(video.webkitEnterFullscreen)video.webkitEnterFullscreen();});
  else if(video.webkitEnterFullscreen)video.webkitEnterFullscreen();
 });
 if(video.hasAttribute('src'))start();
 else if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){start();observer.disconnect();}},{rootMargin:'500px'});observer.observe(stage);}
 else start();
});

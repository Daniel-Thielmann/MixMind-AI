export interface VideoResource {
  src: string;
  poster: string;
  thumbnail: string;
}

export async function preloadVideo(src: string): Promise<HTMLVideoElement> {
  return new Promise((resolve, reject) => {
    const video = document.createElement("video");
    video.preload = "auto";
    video.muted = true;
    video.oncanplaythrough = () => resolve(video);
    video.onerror = () => reject(new Error(`Failed to preload video: ${src}`));
    video.src = src;
    video.load();
  });
}

export async function preloadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error(`Failed to preload image: ${src}`));
    img.src = src;
  });
}

export function canPlayVideo(src: string): boolean {
  const video = document.createElement("video");
  const ext = src.split(".").pop()?.toLowerCase();
  const mimeTypes: Record<string, string> = {
    mp4: "video/mp4",
    webm: "video/webm",
    ogg: "video/ogg",
  };
  const mime = ext ? mimeTypes[ext] : undefined;
  return mime ? !!video.canPlayType(mime) : false;
}

export function getVideoResource(basePath: string): VideoResource {
  const normalized = basePath.replace(/\/+$/, "");
  return {
    src: `${normalized}/clip.mp4`,
    poster: `${normalized}/poster.jpg`,
    thumbnail: `${normalized}/thumbnail.jpg`,
  };
}

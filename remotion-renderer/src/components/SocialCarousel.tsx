import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate, interpolateColors, Easing } from 'remotion';
import { OverlaySlide1 } from './OverlaySlide1';
import { OverlaySlide2 } from './OverlaySlide2';
import { OverlaySlide3 } from './OverlaySlide3';
import { OverlaySlide4 } from './OverlaySlide4';
import { OverlaySlide5 } from './OverlaySlide5';

export const SocialCarousel: React.FC = () => {
	const frame = useCurrentFrame();
	const { fps } = useVideoConfig();

	// 1. Horizontal Page Swipe Translation
	// Transitions happen at:
	// Slide 1 -> 2: frames 105 to 120 (3.5s to 4.0s)
	// Slide 2 -> 3: frames 225 to 240 (7.5s to 8.0s)
	// Slide 3 -> 4: frames 345 to 360 (11.5s to 12.0s)
	// Slide 4 -> 5: frames 465 to 480 (15.5s to 16.0s)
	const translateX = interpolate(
		frame,
		[0, 105, 120, 225, 240, 345, 360, 465, 480, 600],
		[0, 0, -1080, -1080, -2160, -2160, -3240, -3240, -4320, -4320],
		{
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
			easing: Easing.bezier(0.25, 0.1, 0.25, 1),
		}
	);

	// Slide 1 Animations: cover
	// Background: sine-wave breathing scale (1.01 to 1.025)
	const bgScale1 = 1.0175 + 0.0075 * Math.sin((frame * 2 * Math.PI) / 60);

	// Gold script: spring-scale from 0.6 to 1.0, rotate overshoot -5deg to 0deg starting at frame 15
	const springFrame = frame - 15;
	const scriptSpring = spring({
		frame: springFrame,
		fps,
		config: {
			damping: 12,
			stiffness: 100,
			mass: 0.8,
		},
	});
	const scriptScale = interpolate(scriptSpring, [0, 1], [0.6, 1.0]);
	const scriptRotate = interpolate(scriptSpring, [0, 1], [-5, 0]);
	const scriptOpacity = frame < 15 ? 0 : interpolate(frame, [15, 25], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Slide 2 Animations: quote
	// Background: slow zoom 1.0 to 1.05
	const bgScale2 = interpolate(frame, [120, 240], [1.0, 1.05], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	// Typewriter effect: reveal char paths based on frame count (stagger: 0.03s = 0.9 frames per char)
	const getCharOpacity = (index: number) => {
		const startFrame = 120 + index * 0.9;
		return interpolate(frame, [startFrame, startFrame + 3], [0, 1], {
			extrapolateLeft: 'clamp',
			extrapolateRight: 'clamp',
		});
	};

	// Slide 3 Animations: calendar
	// Circle draws starting at 0.5s mark (frame 255)
	const circleProgress = interpolate(frame, [255, 285], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: Easing.bezier(0.25, 0.1, 0.25, 1),
	});

	// Slide 4 Animations: news bento reveal
	// Item 1: slides up and fades in at 12.5s (frame 375)
	const item1Y = interpolate(frame, [375, 390], [20, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: Easing.out(Easing.quad),
	});
	const item1Opacity = interpolate(frame, [375, 390], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Item 2: slides up and fades in at 12.7s (frame 381)
	const item2Y = interpolate(frame, [381, 396], [20, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: Easing.out(Easing.quad),
	});
	const item2Opacity = interpolate(frame, [381, 396], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Item 3: slides up and fades in at 12.9s (frame 387)
	const item3Y = interpolate(frame, [387, 402], [20, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
		easing: Easing.out(Easing.quad),
	});
	const item3Opacity = interpolate(frame, [387, 402], [0, 1], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Slide 5 Animations: outro
	// Transition: color from grey (#808080) to gold (#C5A059) over 1.5 seconds (45 frames, 495 to 540)
	const goldColor = interpolateColors(frame, [495, 540], ['#808080', '#C5A059']);
	// Final glow: drop-shadow once color transition completes (fades in from 540 to 555)
	const glowIntensity = interpolate(frame, [540, 555], [0, 10], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});
	const glowOpacity = interpolate(frame, [540, 555], [0, 0.2], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	// Global Fade to Black (last 15 frames: 585 to 600)
	const globalOpacity = interpolate(frame, [585, 600], [1, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<div
			style={{
				width: 1080,
				height: 1080,
				position: 'relative',
				overflow: 'hidden',
				backgroundColor: '#000',
				opacity: globalOpacity,
			}}
		>
			<div
				style={{
					display: 'flex',
					flexDirection: 'row',
					width: 5400,
					height: 1080,
					transform: `translateX(${translateX}px)`,
				}}
			>
				{/* Slide 1 */}
				<div style={{ width: 1080, height: 1080, position: 'relative', flexShrink: 0 }}>
					<OverlaySlide1
						scriptScale={scriptScale}
						scriptRotate={scriptRotate}
						scriptOpacity={scriptOpacity}
						bgScale={bgScale1}
					/>
				</div>

				{/* Slide 2 */}
				<div style={{ width: 1080, height: 1080, position: 'relative', flexShrink: 0 }}>
					<OverlaySlide2
						getCharOpacity={getCharOpacity}
						bgScale={bgScale2}
					/>
				</div>

				{/* Slide 3 */}
				<div style={{ width: 1080, height: 1080, position: 'relative', flexShrink: 0 }}>
					<OverlaySlide3 circleProgress={circleProgress} />
				</div>

				{/* Slide 4 */}
				<div style={{ width: 1080, height: 1080, position: 'relative', flexShrink: 0 }}>
					<OverlaySlide4
						item1Y={item1Y}
						item2Y={item2Y}
						item3Y={item3Y}
						item1Opacity={item1Opacity}
						item2Opacity={item2Opacity}
						item3Opacity={item3Opacity}
					/>
				</div>

				{/* Slide 5 */}
				<div style={{ width: 1080, height: 1080, position: 'relative', flexShrink: 0 }}>
					<OverlaySlide5
						goldColor={goldColor}
						glowIntensity={glowIntensity}
						glowOpacity={glowOpacity}
					/>
				</div>
			</div>
		</div>
	);
};

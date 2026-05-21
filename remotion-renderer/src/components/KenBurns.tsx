import { Img, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export const KenBurns: React.FC<{ imageUrl: string }> = ({ imageUrl }) => {
	const frame = useCurrentFrame();
	const { durationInFrames } = useVideoConfig();

	// Smooth slow zoom from 1.0 to 1.2 over the duration of the clip
	const scale = interpolate(
		frame,
		[0, durationInFrames],
		[1, 1.2],
		{ extrapolateRight: 'clamp' }
	);

	// Slight pan effect
	const translateX = interpolate(
		frame,
		[0, durationInFrames],
		[0, 50],
		{ extrapolateRight: 'clamp' }
	);

	return (
		<div style={{ flex: 1, backgroundColor: 'black', overflow: 'hidden' }}>
			<Img
				src={imageUrl}
				style={{
					width: '100%',
					height: '100%',
					objectFit: 'cover',
					transform: `scale(${scale}) translateX(${translateX}px)`,
				}}
			/>
		</div>
	);
};

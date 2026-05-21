import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

export const DataOverlay: React.FC<{
	horseName: string;
	sire: string;
	dam: string;
	winRate: string;
}> = ({ horseName, sire, dam, winRate }) => {
	const frame = useCurrentFrame();
	const { fps } = useVideoConfig();

	// Slide in animation using spring physics
	const entrance = spring({
		frame,
		fps,
		config: {
			damping: 12,
		},
	});

	const translateY = interpolate(entrance, [0, 1], [1000, 0]);
	const opacity = interpolate(entrance, [0, 1], [0, 1]);

	return (
		<div style={{ 
			flex: 1, 
			display: 'flex', 
			justifyContent: 'center', 
			alignItems: 'center',
			fontFamily: 'sans-serif',
			backgroundColor: 'transparent'
		}}>
			{/* Glass-morphism Container */}
			<div style={{
				transform: `translateY(${translateY}px)`,
				opacity,
				backgroundColor: 'rgba(255, 255, 255, 0.15)',
				backdropFilter: 'blur(20px)',
				borderRadius: '24px',
				padding: '60px',
				border: '1px solid rgba(255,255,255,0.3)',
				color: 'white',
				boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
				width: '80%',
			}}>
				<h1 style={{ fontSize: '80px', marginBottom: '30px', borderBottom: '4px solid white', paddingBottom: '10px' }}>
					{horseName}
				</h1>
				<div style={{ fontSize: '50px', display: 'flex', flexDirection: 'column', gap: '30px' }}>
					<div style={{ display: 'flex', justifyContent: 'space-between' }}>
						<span style={{ opacity: 0.8 }}>Sire:</span>
						<strong>{sire}</strong>
					</div>
					<div style={{ display: 'flex', justifyContent: 'space-between' }}>
						<span style={{ opacity: 0.8 }}>Dam:</span>
						<strong>{dam}</strong>
					</div>
					<div style={{ display: 'flex', justifyContent: 'space-between' }}>
						<span style={{ opacity: 0.8 }}>Win Rate:</span>
						<strong>{winRate}</strong>
					</div>
				</div>
			</div>
		</div>
	);
};

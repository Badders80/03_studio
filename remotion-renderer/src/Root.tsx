import { Composition } from 'remotion';
import { DataOverlay } from './components/DataOverlay';
import { KenBurns } from './components/KenBurns';
import { SocialCarousel } from './components/SocialCarousel';

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition
				id="SocialCarousel"
				component={SocialCarousel}
				durationInFrames={600}
				fps={30}
				width={1080}
				height={1080}
			/>
			<Composition
				id="DataOverlay"
				component={DataOverlay}
				durationInFrames={150}
				fps={30}
				width={1080}
				height={1920}
				defaultProps={{
					horseName: "Evo Champion",
					sire: "Starlight",
					dam: "Moonbeam",
					winRate: "75%"
				}}
			/>
			<Composition
				id="KenBurns"
				component={KenBurns}
				durationInFrames={150}
				fps={30}
				width={1080}
				height={1920}
				defaultProps={{
					imageUrl: "https://via.placeholder.com/1080x1920"
				}}
			/>
		</>
	);
};

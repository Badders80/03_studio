import { Composition } from 'remotion';
import { DataOverlay } from './components/DataOverlay';
import { KenBurns } from './components/KenBurns';
import { SocialCarousel } from './components/SocialCarousel';
import { Poster } from './components/Poster';

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
			<Composition
				id="Poster"
				component={Poster}
				durationInFrames={1}
				fps={30}
				width={1080}
				height={1350}
				defaultProps={{
					contextTag: "NEXT UP...",
					heroTitle: "Prudentia",
					columnCount: 2,
					col1Primary: "MASA HASHIZUME",
					col1Sublabel: "CONFIRMED JOCKEY",
					col2Primary: "TE RAPA",
					col2Sublabel: "THIS WEEKEND",
					imageSrc: "",
					imageScale: 1.0,
					imageFocusX: 50,
					imageFocusY: 50
				}}
			/>
		</>
	);
};


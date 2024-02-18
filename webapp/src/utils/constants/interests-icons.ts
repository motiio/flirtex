import { FunctionComponent } from 'react';
import { ReactComponent as Airplane } from '../../assets/icons/airplane.svg';
import { ReactComponent as Video } from '../../assets/icons/video-play.svg';
import { ReactComponent as Weight } from '../../assets/icons/weight.svg';
import { ReactComponent as Cake } from '../../assets/icons/cake.svg';
import { ReactComponent as MusicNote } from '../../assets/icons/music-note.svg';
import { ReactComponent as Gallery } from '../../assets/icons/gallery.svg';
import { ReactComponent as Camera } from '../../assets/icons/camera.svg';
import { ReactComponent as Tree } from '../../assets/icons/tree.svg';
import { ReactComponent as Code } from '../../assets/icons/code.svg';
import { ReactComponent as Book } from '../../assets/icons/book.svg';
import { ReactComponent as Pet } from '../../assets/icons/pet.svg';
import { ReactComponent as Heart } from '../../assets/icons/heart.svg';
import { ReactComponent as Triangle } from '../../assets/icons/triangle.svg';
import { ReactComponent as Coffee } from '../../assets/icons/coffee.svg';
import { ReactComponent as Car } from '../../assets/icons/car.svg';

export const InterestsIcons: {
  [key: string]: FunctionComponent;
} = {
  '4d5e24f2-8e2c-4ee3-a54b-a4d8ec02ddb8': Airplane,
  '21cf46fe-f082-4380-bd02-92d91e094edd': Video,
  '4001c3fe-d68c-4b39-8253-ac6ed5d380ba': Heart,
  '33a3d79d-c8a0-4cbf-8bb6-399ea99b01b4': Cake,
  '20fc0274-ddca-4725-93bf-9543a00074e9': MusicNote,
  '3b728363-7730-470e-afd7-a304bcbeaad7': Camera,
  '0dfda286-6190-4cef-bb10-693ffb80fbdb': Gallery,
  '163220c6-9e9a-4d11-b8a3-d7f538cc0297': Book,
  'a7d44f8c-0ed1-42ba-83fe-81bf6c4513af': Car,
  '427643b0-c96b-466a-aa8f-026fe718cac0': Code,
  'a24dff76-2240-41ca-a98d-76baea350666': Triangle,
  '7993e3f2-0731-49b8-ada3-d8c3f656e906': Weight,
  '6985c51b-181d-4afc-b4a7-819fcb0c45dd': Coffee,
  '41c1639f-ffa7-4c6b-9787-a1552774f740': Pet,
  '05f420c0-4967-4570-b547-3ec21d6f82e3': Tree,
};

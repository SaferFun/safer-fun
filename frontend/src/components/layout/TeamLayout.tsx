import Image, { StaticImageData } from "next/image";
import alper from "../../public/image/alper.png";
import adam from "../../public/image/adam.png";
import eren from "../../public/image/eren.png";
import walid from "../../public/image/walid.png";

interface TeamMember {
  id: number;
  name: string;
  role: string;
  bio: string;
  study: string;
  contentOne: string;
  contentTwo: string;
  contentThree?: string;
  image: StaticImageData;
  height?: number;
}

const teamMembers: TeamMember[] = [
  {
    id: 1,
    name: "Adam Bouabda",
    role: "Researcher",
    study: "ETHZ Msc Maths / EPFL Bsc Maths",
    bio: "Hackathons*Rewards*Research",
    contentOne: "EPFL Sui hackathon winner -> Dex",
    contentTwo:"Sui Academic Research Awards batch 2 for DeFi and AI,",
    contentThree: "Uniswap Foundation Fellow Researcher on Dynamic CFMMs. ETHZ Research assistant in Stochastic Finance Group. ETHZ Research assistant in Statistics Chair",
    image:adam,
    height: 210
  },
  {
    id: 2,
    name: "Alper Özyurt",
    role: "Blockchain / Backend Dev & Researcher",
    study: "EPFL Bsc CS",
    bio:"Hackathons*Experience*Extras",
    contentOne: "EPFL Sui hackathon winner -> Dex. EthDam Finalist -> Blockchain Security. EthGlobal Hyperlane winner -> Dex. Solana Speedrun winner -> NFT/Token ",
    contentTwo:"1.5 years of full-stack freelancing on web & blockchain applications. 1 year of head blockchain developer/engineer at AFEL & IronNode on Solana (on-going)",
    contentThree:"Some other side projects on different chains like Sui, EVM and Polygon. Tool development for games",
    image:alper

  },
  {
    id: 3,
    name: "Walid Sofiane",
    role: "Researcher",
    study: "EPFL Msc INGEFIN / Bsc Maths",
    bio:"Hackathons*Reasearch Awards*Extras",
    contentOne: "EPFL Sui hackathon winner -> Dex. RiskOn hackathon winner -> AI and private banking",
    contentTwo: "SUI Academic research awards batch 1 for Defi and AI. SUI Academic research awards batch 2 for Defi and AI.",
    contentThree:"Currently intern at Cadena platforms as data analyst and ML engineer",
    image:walid
  },
  {
    id: 4,
    name: "Erengazi Mutlu",
    study:"Bilkent University Bsc CS",
    role: "Bakcend / Frontend Dev",
    bio: "Experience*Projects",
    contentOne: "1.5 year full-time web development. 4 months software developer/engineer at AFEL.",
    contentTwo:"Blockchain-Based Product Tracking System project using web technologies. Custom Thread Library Implementation in C, using x86 Assembly for low-level thread management and scheduling.",
    image:eren
  },
];

export default function TeamLayout() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center text-theme-text">
        Team
      </h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {teamMembers.map((member) => (
          <div
            key={member.id}
            className="bg-theme-bg rounded-lg shadow-2xl p-6 flex flex-col items-center text-theme-text"
          >
            <Image height={member.height?member.height:200} alt="" src={member.image}></Image>
            <h2 className="text-2xl font-semibold mb-2">{member.name}</h2>
            <p className="text-xl text-theme-text/70 mb-2">{member.study}</p>
            <p className="text-lg text-theme-text/70 mb-2">{member.role}</p>
            <p className="text-theme-text/70 mb-2">{member.bio.split("*")[0]}</p>
            <ul className="list-disc list-inside text-left">
              {member.contentOne.split('. ').map((sentence, index) => (
              <li key={index}>{sentence}</li>
              ))}
            </ul>
            
            <p className="text-theme-text/70 mb-2">{member.bio.split("*")[1]}</p>
            <ul className="list-disc list-inside text-left">
              {member.contentTwo.split('. ').map((sentence, index) => (
              <li key={index}>{sentence}</li>
              ))}
            </ul>

            {member.contentThree && (
              <>
                <p className="text-theme-text/70 mb-2">{member.bio.split("*")[2]}</p>
                <ul className="list-disc list-inside text-left">
                  {member.contentThree.split('. ').map((sentence, index) => (
                    <li key={index}>{sentence}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

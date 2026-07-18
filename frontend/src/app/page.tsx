import { Hero } from "@/components/landing/Hero";
import { HowItWorks } from "@/components/landing/HowItWorks";
import { UploadSection } from "@/components/landing/UploadSection";
import { Demonstration } from "@/components/landing/Demonstration";
import { TransitionRecommendation } from "@/components/landing/TransitionRecommendation";
import { DataSciencePreview } from "@/components/landing/DataSciencePreview";
import { Features } from "@/components/landing/Features";
import { Pricing } from "@/components/landing/Pricing";
import { Footer } from "@/components/landing/Footer";

export default function Home() {
  return (
    <>
      <Hero />
      <HowItWorks />
      <UploadSection />
      <Demonstration />
      <TransitionRecommendation />
      <DataSciencePreview />
      <Features />
      <Pricing />
      <Footer />
    </>
  );
}

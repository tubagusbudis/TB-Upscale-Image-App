import { motion } from "framer-motion";

const BouncyText = ({ text = "Bouncy Animation", className = "" }: { text?: string, className?: string }) => {
    return (
        <h1 className={className}>
            {text.split('').map((char, i) => (
                <motion.span
                    key={i}
                    initial={{ y: 0 }}
                    animate={{ 
                        y: [0, -10, 0], // Reduced bounce slightly to fit nicely as a title
                        transition: {
                            delay: i * 0.1,
                            duration: 0.6,
                            repeat: Infinity,
                            repeatDelay: 2,
                            ease: "easeInOut"
                        }
                    }}
                    className="inline-block"
                >
                    {char === ' ' ? '\u00A0' : char}
                </motion.span>
            ))}
        </h1>
    );
};

export default BouncyText;

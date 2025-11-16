#!/usr/bin/env python3
"""
Password List Generator - Complete Tool
A comprehensive password wordlist generator for security testing
Author: Your Name
Version: 1.0.0
"""

import itertools
import random
import string
import json
import os
import argparse
import time
from typing import List, Dict, Any

class Banner:
    @staticmethod
    def show_main_banner():
        """Display main banner"""
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ║
║    ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗║
║    ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝║
║    ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗║
║    ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║║
║    ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝║
║                                                                ║
║              ██╗     ██╗███████╗████████╗                     ║
║              ██║     ██║██╔════╝╚══██╔══╝                     ║
║              ██║     ██║███████╗   ██║                        ║
║              ██║     ██║╚════██║   ██║                        ║
║              ███████╗██║███████║   ██║                        ║
║              ╚══════╝╚═╝╚══════╝   ╚═╝                        ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                 PASSWORD WORDLIST GENERATOR                   ║
║                      Version 1.0.0                            ║
║                Created for Educational Purposes               ║
╚════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    @staticmethod
    def show_generation_banner(wordlist_name: str, count: int):
        """Display generation banner"""
        banner = f"""
╔════════════════════════════════════════════════════════════════╗
║                       GENERATING WORDLIST                     ║
╠════════════════════════════════════════════════════════════════╣
║  Wordlist Name: {wordlist_name:<35} ║
║  Target Count:  {count:<35} ║
║  Started At:    {time.strftime('%Y-%m-%d %H:%M:%S'):<35} ║
╚════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    @staticmethod
    def show_completion_banner(filename: str, count: int, analysis: Dict):
        """Display completion banner"""
        banner = f"""
╔════════════════════════════════════════════════════════════════╗
║                      GENERATION COMPLETE                      ║
╠════════════════════════════════════════════════════════════════╣
║  Output File:   {filename:<35} ║
║  Total Passwords: {count:<34} ║
║  Average Length: {analysis['avg_length']:<34} ║
║  Average Entropy: {analysis['entropy_stats']['avg']:<33} ║
║  Completed At:  {time.strftime('%Y-%m-%d %H:%M:%S'):<35} ║
╚════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    @staticmethod
    def show_level_banner(level: str):
        """Display level-specific banner"""
        level_banners = {
            'beginner': """
╔════════════════════════════════════════════════════════════════╗
║                      BEGINNER LEVEL                           ║
╠════════════════════════════════════════════════════════════════╣
║  Generating simple passwords, common patterns, and           ║
║  basic keyboard walks...                                      ║
╚════════════════════════════════════════════════════════════════╝
""",
            'intermediate': """
╔════════════════════════════════════════════════════════════════╗
║                     INTERMEDIATE LEVEL                        ║
╠════════════════════════════════════════════════════════════════╣
║  Generating passwords with special characters,               ║
║  number combinations, and basic leet speak...                ║
╚════════════════════════════════════════════════════════════════╝
""",
            'advanced': """
╔════════════════════════════════════════════════════════════════╗
║                       ADVANCED LEVEL                          ║
╠════════════════════════════════════════════════════════════════╣
║  Generating complex leet speak, random patterns,            ║
║  and high-entropy passwords...                               ║
╚════════════════════════════════════════════════════════════════╝
""",
            'all': """
╔════════════════════════════════════════════════════════════════╗
║                    COMPREHENSIVE MODE                         ║
╠════════════════════════════════════════════════════════════════╣
║  Generating passwords across all levels:                     ║
║  Beginner → Intermediate → Advanced                         ║
╚════════════════════════════════════════════════════════════════╝
"""
        }
        print(level_banners.get(level, ""))

    @staticmethod
    def show_legal_warning():
        """Display legal warning banner"""
        warning = """
╔════════════════════════════════════════════════════════════════╗
║                       ⚠️  LEGAL WARNING ⚠️                      ║
╠════════════════════════════════════════════════════════════════╣
║  This tool is for:                                            ║
║    • Educational purposes                                     ║
║    • Authorized security testing                             ║
║    • Personal security awareness                              ║
║                                                              ║
║  ❌ NEVER use for unauthorized activities                     ║
║  ✅ ALWAYS get proper permission                              ║
║  ✅ FOLLOW local laws and regulations                         ║
║                                                              ║
║  By using this tool, you agree to use it responsibly         ║
╚════════════════════════════════════════════════════════════════╝
"""
        print(warning)

class PasswordListGenerator:
    def __init__(self):
        self.common_special_chars = '!@#$%^&*'
        
    def generate_leet_speak(self, word: str, custom_mapping: Dict = None) -> List[str]:
        """Generate leet speak variations of a word"""
        if custom_mapping is None:
            custom_mapping = {
                'a': ['4', '@'],
                'e': ['3'],
                'i': ['1', '!'],
                'o': ['0'],
                's': ['5', '$'],
                't': ['7']
            }
        
        variations = [word]
        
        for char, replacements in custom_mapping.items():
            new_variations = []
            for variation in variations:
                if char in variation.lower():
                    for replacement in replacements:
                        new_variations.append(variation.lower().replace(char, replacement))
                        new_variations.append(variation.capitalize().replace(char, replacement))
            variations.extend(new_variations)
        
        return list(dict.fromkeys(variations))
    
    def generate_keyboard_patterns(self, length: int = 8) -> List[str]:
        """Generate keyboard walk patterns"""
        patterns = []
        
        keyboard_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm'
        ]
        
        for row in keyboard_rows:
            for i in range(len(row) - length + 1):
                patterns.append(row[i:i+length])
                patterns.append(row[i:i+length][::-1])
        
        common_patterns = [
            '1qaz2wsx', '1q2w3e4r', '1q2w3e4r5t',
            'qazwsxedc', 'zaq12wsx', '!qaz@wsx'
        ]
        patterns.extend(common_patterns)
        
        return patterns
    
    def generate_beginner_passwords(self, count=100) -> List[str]:
        """Generate beginner level passwords"""
        print("🔰 Generating beginner passwords...")
        passwords = []
        
        common = [
            '123456', 'password', '12345678', 'qwerty', '123456789',
            '12345', '1234', '111111', '1234567', 'dragon', '123123',
            'baseball', 'abc123', 'football', 'monkey', 'letmein',
            'shadow', 'master', '666666', 'qwertyuiop', '123321',
            'mustang', '1234567890', 'michael', '654321', 'superman',
            '1qaz2wsx', '7777777', '121212', '000000'
        ]
        passwords.extend(common)
        
        for i in range(100, 1000):
            passwords.append(f"pass{i}")
            passwords.append(f"test{i}")
            passwords.append(f"admin{i}")
        
        keyboard_patterns = self.generate_keyboard_patterns()
        passwords.extend(keyboard_patterns)
        
        return passwords[:count]
    
    def generate_intermediate_passwords(self, keywords: List[str] = None, count=200) -> List[str]:
        """Generate intermediate level passwords"""
        print("🔸 Generating intermediate passwords...")
        if keywords is None:
            keywords = ['user', 'admin', 'test']
        
        passwords = []
        special_chars = ['!', '@', '#', '$', '%']
        
        for keyword in keywords:
            for i in range(100, 1000):
                passwords.append(f"{keyword}{i}")
                passwords.append(f"{keyword}{i}!")
            
            for char in special_chars:
                passwords.append(f"{keyword}{char}123")
                passwords.append(f"{keyword}123{char}")
        
        common_words = ['hello', 'welcome', 'sunshine', 'dragon', 'shadow']
        for word in common_words:
            for i in range(100, 500):
                passwords.append(f"{word}{i}")
        
        return passwords[:count]
    
    def generate_advanced_passwords(self, keywords: List[str] = None, count=300) -> List[str]:
        """Generate advanced level passwords"""
        print("🔷 Generating advanced passwords...")
        if keywords is None:
            keywords = ['admin', 'user', 'secure']
        
        passwords = []
        
        for keyword in keywords:
            leet_variations = self.generate_leet_speak(keyword)
            passwords.extend(leet_variations)
            
            for variation in leet_variations[:5]:
                for year in [2020, 2021, 2022, 2023, 2024]:
                    passwords.append(f"{variation}{year}")
                    passwords.append(f"{variation}_{year}")
                    passwords.append(f"{variation}@{year}")
        
        for _ in range(50):
            length = random.randint(8, 12)
            password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%', k=length))
            passwords.append(password)
        
        return passwords[:count]
    
    def generate_name_based_passwords(self, names: List[str], count=200) -> List[str]:
        """Generate passwords based on names"""
        print("👤 Generating name-based passwords...")
        passwords = []
        
        for name in names:
            passwords.extend([
                name.lower(),
                name.capitalize(),
                name.lower() + '123',
                name.capitalize() + '123',
                name.lower() + '2024',
                name.capitalize() + '2024'
            ])
            
            leet_name = self.generate_leet_speak(name.lower())
            passwords.extend(leet_name)
            
            for char in ['!', '@', '#', '$']:
                passwords.append(f"{name.lower()}{char}123")
                passwords.append(f"{name.capitalize()}{char}123")
                passwords.append(f"{name.lower()}{char}2024")
        
        return passwords[:count]
    
    def generate_comprehensive_list(self, keywords: List[str] = None, names: List[str] = None, 
                                  total_count=1000) -> List[str]:
        """Generate comprehensive password list from beginner to advanced"""
        all_passwords = []
        
        beginner = self.generate_beginner_passwords(int(total_count * 0.2))
        all_passwords.extend(beginner)
        
        intermediate = self.generate_intermediate_passwords(keywords, int(total_count * 0.3))
        all_passwords.extend(intermediate)
        
        advanced = self.generate_advanced_passwords(keywords, int(total_count * 0.3))
        all_passwords.extend(advanced)
        
        if names:
            name_based = self.generate_name_based_passwords(names, int(total_count * 0.2))
            all_passwords.extend(name_based)
        
        return list(dict.fromkeys(all_passwords))[:total_count]

    def generate_custom_pattern(self, base_words: List[str], patterns: List[str]) -> List[str]:
        """Generate passwords based on custom patterns"""
        print("🎨 Generating custom pattern passwords...")
        passwords = []
        
        for word in base_words:
            for pattern in patterns:
                if '{word}' in pattern:
                    passwords.append(pattern.replace('{word}', word))
                else:
                    passwords.append(word + pattern)
                    passwords.append(pattern + word)
        
        return list(dict.fromkeys(passwords))

class PasswordUtils:
    @staticmethod
    def save_wordlist(passwords: List[str], filename: str, format_type: str = 'txt'):
        """Save password list to file"""
        
        if format_type == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                for password in passwords:
                    f.write(f"{password}\n")
        
        elif format_type == 'json':
            data = {
                'metadata': {
                    'total_passwords': len(passwords),
                    'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'wordlist_name': os.path.splitext(filename)[0]
                },
                'passwords': passwords
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        
        print(f"💾 Wordlist saved to {filename} with {len(passwords)} passwords")

    @staticmethod
    def load_keywords(filename: str) -> List[str]:
        """Load keywords from file"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        return []

    @staticmethod
    def load_names(filename: str) -> List[str]:
        """Load names from file"""
        return PasswordUtils.load_keywords(filename)

    @staticmethod
    def calculate_entropy(password: str) -> float:
        """Calculate password entropy"""
        char_set = 0
        if any(c.islower() for c in password):
            char_set += 26
        if any(c.isupper() for c in password):
            char_set += 26
        if any(c.isdigit() for c in password):
            char_set += 10
        if any(c in '!@#$%^&*' for c in password):
            char_set += 8
        
        if char_set == 0:
            return 0
        
        entropy = len(password) * (char_set ** 0.5)
        return round(entropy, 2)

    @staticmethod
    def analyze_wordlist(passwords: List[str]) -> Dict[str, Any]:
        """Analyze password list"""
        analysis = {
            'total_passwords': len(passwords),
            'avg_length': 0,
            'min_length': float('inf'),
            'max_length': 0,
            'entropy_stats': {
                'min': float('inf'),
                'max': 0,
                'avg': 0
            }
        }
        
        total_length = 0
        total_entropy = 0
        
        for password in passwords:
            length = len(password)
            total_length += length
            analysis['min_length'] = min(analysis['min_length'], length)
            analysis['max_length'] = max(analysis['max_length'], length)
            
            entropy = PasswordUtils.calculate_entropy(password)
            total_entropy += entropy
            analysis['entropy_stats']['min'] = min(analysis['entropy_stats']['min'], entropy)
            analysis['entropy_stats']['max'] = max(analysis['entropy_stats']['max'], entropy)
        
        analysis['avg_length'] = round(total_length / len(passwords), 2)
        analysis['entropy_stats']['avg'] = round(total_entropy / len(passwords), 2)
        
        return analysis

def basic_example():
    """Basic example usage"""
    Banner.show_main_banner()
    Banner.show_legal_warning()
    
    print("🚀 Starting Basic Example...")
    
    generator = PasswordListGenerator()
    utils = PasswordUtils()
    
    names = ['dipti', 'pal', 'diptipal']
    keywords = ['admin', 'user', 'secure', 'password']
    
    Banner.show_generation_banner("Dipti_Pal_Wordlist", 1000)
    Banner.show_level_banner('all')
    
    passwords = generator.generate_comprehensive_list(
        keywords=keywords,
        names=names,
        total_count=1000
    )
    
    utils.save_wordlist(passwords, 'dipti_password_list.txt')
    
    analysis = utils.analyze_wordlist(passwords)
    Banner.show_completion_banner('dipti_password_list.txt', len(passwords), analysis)
    
    print("\n📋 Sample passwords (first 20):")
    print("-" * 40)
    for i, pwd in enumerate(passwords[:20]):
        print(f"{i+1:2d}. {pwd}")

def advanced_example():
    """Advanced example with custom patterns"""
    Banner.show_main_banner()
    
    print("🚀 Starting Advanced Example...")
    
    generator = PasswordListGenerator()
    utils = PasswordUtils()
    
    custom_patterns = [
        '{word}123!@#',
        '{word}_2024_secure',
        'admin_{word}_pass',
        '{word}@company.com',
        'Spring2024{word}',
        '{word}!QAZ2wsx'
    ]
    
    base_words = ['dipti', 'pal', 'admin', 'user']
    
    Banner.show_generation_banner("Custom_Pattern_Wordlist", 300)
    
    custom_passwords = generator.generate_custom_pattern(base_words, custom_patterns)
    beginner = generator.generate_beginner_passwords(50)
    advanced = generator.generate_advanced_passwords(['dipti', 'pal'], 100)
    
    all_passwords = list(dict.fromkeys(beginner + advanced + custom_passwords))
    
    utils.save_wordlist(all_passwords, 'custom_wordlist.txt')
    utils.save_wordlist(all_passwords, 'custom_wordlist.json', 'json')
    
    analysis = utils.analyze_wordlist(all_passwords)
    Banner.show_completion_banner('custom_wordlist.txt', len(all_passwords), analysis)

def cli_interface():
    """Command Line Interface"""
    Banner.show_main_banner()
    Banner.show_legal_warning()
    
    parser = argparse.ArgumentParser(description='Generate password wordlists')
    
    parser.add_argument('-o', '--output', default='password_list.txt',
                       help='Output filename')
    parser.add_argument('-c', '--count', type=int, default=1000,
                       help='Total number of passwords to generate')
    parser.add_argument('--format', choices=['txt', 'json'], default='txt',
                       help='Output format')
    
    parser.add_argument('--keywords', nargs='+', help='Keywords for password generation')
    parser.add_argument('--names', nargs='+', help='Names for password generation')
    parser.add_argument('--level', choices=['beginner', 'intermediate', 'advanced', 'all'],
                       default='all', help='Password complexity level')
    
    parser.add_argument('--keywords-file', help='File containing keywords')
    parser.add_argument('--names-file', help='File containing names')
    
    parser.add_argument('--example', action='store_true', help='Run basic example')
    parser.add_argument('--advanced-example', action='store_true', help='Run advanced example')
    
    parser.add_argument('--no-banner', action='store_true', help='Hide banners')
    
    args = parser.parse_args()
    
    if args.no_banner:
        # Minimal output without banners
        pass
    else:
        Banner.show_main_banner()
        Banner.show_legal_warning()
    
    if args.example:
        basic_example()
        return
    
    if args.advanced_example:
        advanced_example()
        return
    
    # Load data from files if provided
    keywords = args.keywords or []
    names = args.names or []
    
    if args.keywords_file:
        keywords.extend(PasswordUtils.load_keywords(args.keywords_file))
    
    if args.names_file:
        names.extend(PasswordUtils.load_names(args.names_file))
    
    # Initialize generator
    generator = PasswordListGenerator()
    utils = PasswordUtils()
    
    wordlist_name = os.path.splitext(args.output)[0]
    
    if not args.no_banner:
        Banner.show_generation_banner(wordlist_name, args.count)
        Banner.show_level_banner(args.level)
    
    # Generate based on level
    if args.level == 'all':
        passwords = generator.generate_comprehensive_list(
            keywords=keywords if keywords else None,
            names=names if names else None,
            total_count=args.count
        )
    elif args.level == 'beginner':
        passwords = generator.generate_beginner_passwords(args.count)
    elif args.level == 'intermediate':
        passwords = generator.generate_intermediate_passwords(keywords, args.count)
    elif args.level == 'advanced':
        passwords = generator.generate_advanced_passwords(keywords, args.count)
    
    # Save output
    utils.save_wordlist(passwords, args.output, args.format)
    
    # Show analysis
    analysis = utils.analyze_wordlist(passwords)
    
    if not args.no_banner:
        Banner.show_completion_banner(args.output, len(passwords), analysis)
    else:
        print(f"✓ Generated {analysis['total_passwords']} passwords")
        print(f"✓ Saved to {args.output}")
        print(f"✓ Average entropy: {analysis['entropy_stats']['avg']}")

def main():
    """Main function"""
    try:
        if len(os.sys.argv) > 1:
            cli_interface()
        else:
            Banner.show_main_banner()
            Banner.show_legal_warning()
            
            print("\n" + "="*60)
            print("🎯 No arguments provided. Running examples...")
            print("="*60)
            
            basic_example()
            
            print("\n" + "="*60)
            print("🔧 For command line usage, run:")
            print("   python password_generator.py --help")
            print("="*60)
            
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n\n💥 Error occurred: {e}")

if __name__ == "__main__":
    main()

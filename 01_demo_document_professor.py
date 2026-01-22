from core.document_processor import DocumentProcessor


def main():
    print("Program started")

    print("Preparing sample document content...")
    sample_content = """
# Cricket and the Legacy of Rohit Sharma

Cricket is more than just a sport; it is a culture, a passion, and for millions of people around the world, a way of life. Originating in England, cricket has evolved into one of the most popular sports globally, especially in countries like India, Australia, England, Pakistan, South Africa, Sri Lanka, and the West Indies. Over the years, cricket has produced legendary players who have inspired generations. Among modern-era cricketers, Rohit Sharma stands out as one of the finest batsmen and leaders the game has ever seen. His journey, achievements, and impact on Indian cricket make him a central figure in the story of contemporary cricket.

## Understanding the Game of Cricket

Cricket is played between two teams of eleven players each. The game is primarily played in three formats: Test cricket, One Day Internationals (ODIs), and Twenty20 (T20) cricket. Test cricket is considered the purest form, testing a player’s technique, patience, and endurance over five days. ODIs, played over 50 overs per side, balance strategy and aggression, while T20 cricket, with just 20 overs per side, emphasizes power-hitting and quick decision-making.

The objective of cricket is simple in principle: score more runs than the opposing team. However, the methods, strategies, and skills involved make it a deeply complex and fascinating sport. Batsmen aim to score runs, bowlers try to dismiss batsmen, and fielders support both by stopping runs and taking catches. Team coordination, mental strength, and adaptability are crucial elements that define success in cricket.

## India’s Deep Connection with Cricket

In India, cricket is not merely a sport; it is an emotion that unites people across regions, languages, and cultures. From streets and playgrounds to massive international stadiums, cricket is played and celebrated everywhere. Indian cricket has produced iconic players such as Kapil Dev, Sachin Tendulkar, Rahul Dravid, MS Dhoni, Virat Kohli, and Rohit Sharma. Each of these players has contributed uniquely to India’s cricketing identity, but Rohit Sharma’s elegance, consistency, and leadership have given him a special place among fans.

## Early Life and Background of Rohit Sharma

Rohit Gurunath Sharma was born on April 30, 1987, in Bansod, Nagpur, Maharashtra. Coming from a modest background, Rohit’s early life was marked by financial challenges. His talent for cricket was evident from a young age, and he received support from coaches who recognized his natural ability. He initially started as an off-spin bowler but soon transitioned into a top-order batsman due to his exceptional batting skills.

Rohit’s journey through domestic cricket, especially his performances in the Ranji Trophy, paved the way for his entry into international cricket. His calm demeanor and stylish batting technique quickly caught the attention of selectors and fans alike.

## International Career and Rise to Stardom

Rohit Sharma made his international debut for India in 2007 in a One Day International. While his early career showed flashes of brilliance, consistency remained a challenge. The turning point in his career came when he was promoted to open the innings in limited-overs cricket. This decision transformed Rohit into one of the most destructive and dependable opening batsmen in the world.

Rohit Sharma is widely known for his ability to score big hundreds. He is the only player in history to have scored three double centuries in ODIs, a remarkable achievement that highlights his capacity for long innings and sustained concentration. His elegant stroke play, especially his pull shots, cover drives, and effortless six-hitting ability, has earned him the nickname “Hitman.”

## Achievements and Records

Rohit Sharma’s list of achievements is extensive and impressive. He holds the record for the highest individual score in an ODI match, with 264 runs against Sri Lanka in 2014. He has also scored multiple centuries in World Cup tournaments, proving his ability to perform on the biggest stages. In T20 internationals, Rohit has been one of the most successful batsmen, consistently providing strong starts for the Indian team.

In the Indian Premier League (IPL), Rohit Sharma’s impact has been equally significant. As the captain of the Mumbai Indians, he has led the team to multiple IPL titles, making him one of the most successful captains in the history of the tournament. His leadership skills, tactical awareness, and ability to remain calm under pressure have been key factors behind his success.

## Leadership and Captaincy

Rohit Sharma’s leadership style is often described as composed and strategic. Unlike aggressive leaders, he leads by example and trusts his players. His understanding of the game allows him to make smart decisions, whether it is rotating bowlers, setting fields, or managing player workloads. As the captain of the Indian national team in various formats, Rohit has emphasized teamwork, discipline, and adaptability.

Under his leadership, younger players have been given opportunities to grow and express themselves. Rohit’s mentorship has helped shape the next generation of Indian cricketers, ensuring a strong future for the team.

## Batting Style and Technique

What sets Rohit Sharma apart as a batsman is his timing and balance. He is known for making batting look effortless, often scoring boundaries without excessive force. His ability to play both pace and spin with equal confidence makes him a versatile and dangerous batsman. Rohit is particularly effective in the middle and latter stages of an innings, where his experience allows him to accelerate scoring while minimizing risks.

## Impact Beyond the Field

Beyond his on-field performances, Rohit Sharma has become a role model for aspiring cricketers. His journey from humble beginnings to international stardom inspires young players to believe in their dreams. Rohit is also involved in various charitable initiatives and uses his platform to raise awareness about wildlife conservation and social causes.

## Conclusion

Cricket continues to evolve with time, but its essence remains rooted in skill, strategy, and sportsmanship. Players like Rohit Sharma represent the modern spirit of the game, combining traditional techniques with contemporary aggression. His contributions as a batsman, leader, and role model have left an indelible mark on Indian and world cricket. As fans continue to witness his performances, Rohit Sharma’s legacy in cricket will be remembered as one of excellence, resilience, and inspiration for generations to come.
"""

    with open("sample_file.txt", "w", encoding="utf-8") as file:
        file.write(sample_content)


    print("Initializing DocumentProcessor...")
    processor = DocumentProcessor(chunk_size=300, chunk_overlap=50)
    print("DocumentProcessor initialized successfully")

    print("Starting document loading and chunking...")
    # chunks = processor.process(file_path="sample_file.txt")
    file_path = input('Enter Your File Path : ')
    chunks = processor.process(file_path=file_path)
    print("Document loading and chunking completed")

    print(f"Total chunks created: {len(chunks)}")

    print("Printing chunk details...")
    for index, chunk in enumerate(chunks, start=1):
        print(f"\nChunk Number: {index}")
        print(f"Chunk Size: {len(chunk.page_content)}")
        print(f"Chunk Content Preview: {chunk.page_content[:150]}")
        print(f"Chunk Metadata: {chunk.metadata}")

    print("\nAll chunks processed successfully")
    print("Program execution finished")


if __name__ == "__main__":
    main()

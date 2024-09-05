//
//  SoundPlayer.swift
//  Finger Drums
//
//  Created by v on 2024-09-02.
//

import AVFoundation

class SoundPlayer: NSObject, AVAudioPlayerDelegate { // inherits NSObject, implements? AVAudio...
    private var audioPlayers: [AVAudioPlayer] = [] // arr type AVAudioPlayer
    
    func playSound(file: String) {
        guard let soundURL = locateSoundFile(file) else {
            // if soundURL is nil
            print("Sound file not found")
            return
        }
        
        do {
            let audioPlayer = try AVAudioPlayer(contentsOf: soundURL)
            audioPlayer.delegate = self
            audioPlayer.prepareToPlay()
            audioPlayer.play()
            audioPlayers.append(audioPlayer)
        } catch {
            print("Failed to play sound: \(error.localizedDescription)")
        }
    }
    
    private func locateSoundFile(_ fileName: String) -> URL? {
        return Bundle.main.url(forResource: fileName, withExtension: nil)
    }
    
    func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        if let index = audioPlayers.firstIndex(of: player) {
            audioPlayers.remove(at: index)
        }
    }
}


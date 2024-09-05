//
//  ContentView.swift
//  Finger Drums
//
//  Created by v on 2024-09-02.
//

import SwiftUI

struct ContentView: View {
    let soundPlayer = SoundPlayer()
    @Environment(\.colorScheme) var colorScheme

    var body: some View {
        HStack {
            VStack {
                createButton(soundFile: "snare.wav", imageName: "snare")
                Text(keyboardMappings["snare", default:""])
                createButton(soundFile: "crash.wav", imageName: "crash")
                Text(keyboardMappings["crash", default: ""])
            }
            VStack {
                createButton(soundFile: "closed-hi-hat.wav", imageName: "closed-hi-hat")
                Text(keyboardMappings["closed-hi-hat", default: ""])
                createButton(soundFile: "open-hi-hat.wav", imageName: "open-hi-hat")
                Text(keyboardMappings["open-hi-hat", default: ""])
            }
            VStack {
                createButton(soundFile: "kick.wav", imageName: "kick")
                Text(keyboardMappings["kick", default: ""])
            }
        }
        .padding(.all)
        .frame(width: 300.0, height: 300.0)
    }
    

    let keyboardMappings: [String: String] = [
        "snare": "j",
        "closed-hi-hat": "k",
        "open-hi-hat": "l",
        "crash": "u",
        "kick": "h"
    ]

    func createButton (soundFile: String, imageName: String) -> some View {
        let keyboardShortcut = keyboardMappings[imageName] ?? ""
        
        return Button (action: {
            soundPlayer.playSound(file: soundFile)
        }) {
            Image(imageName).resizable().aspectRatio(contentMode: .fit)
        }
        .buttonStyle(.plain)
        .padding(.all)
        .applyColorInvert(colorScheme)
        .keyboardShortcut(KeyEquivalent(Array(keyboardShortcut)[0]), modifiers: [])
    }
    

}

extension View {

    
    func applyColorInvert(_ colorScheme: ColorScheme) -> some View {
        if colorScheme == .dark {
            return AnyView(self.colorInvert())
        }
        else {
            return AnyView(self)
        }
    }

}

#Preview {
    ContentView()
}

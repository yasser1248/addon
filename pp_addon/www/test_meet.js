window.onload = () => {
        
    const api = new window.JitsiMeetExternalAPI('meet.jit.si', {
    roomName: 'bwb-bfqi-vmg',
    //jwt: 'eyJraWQiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTZmMDk0MTc2ODk2NGFiMzgwZWQwZmJhZGE3YTUwMmYvMGQ4ODVjLVNBTVBMRV9BUFAiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJqaXRzaSIsImV4cCI6MTYxNDAwNTI4OCwibmJmIjoxNjEzOTk4MDgzLCJpc3MiOiJjaGF0Iiwicm9vbSI6IioiLCJzdWIiOiJ2cGFhcy1tYWdpYy1jb29raWUtOTZmMDk0MTc2ODk2NGFiMzgwZWQwZmJhZGE3YTUwMmYiLCJjb250ZXh0Ijp7ImZlYXR1cmVzIjp7ImxpdmVzdHJlYW1pbmciOmZhbHNlLCJvdXRib3VuZC1jYWxsIjpmYWxzZSwidHJhbnNjcmlwdGlvbiI6ZmFsc2UsInJlY29yZGluZyI6ZmFsc2V9LCJ1c2VyIjp7Im1vZGVyYXRvciI6dHJ1ZSwibmFtZSI6IlRlc3QgVXNlciIsImlkIjoiYXV0aDB8NWY5MDNkN2E3N2YzYjQwMDZlYjhlNjdkIiwiYXZhdGFyIjoiIiwiZW1haWwiOiJ0ZXN0LnVzZXJAY29tcGFueS5jb20ifX19.XZTZVSVeFgGNim8YZKLwt37mcc8xkf3oSjuR28KeW8If1Xq5XI7w7K2GnsqZjF0S4XbmZzsswmfh2m9UI7Od_p3USv95Xq6gRjS6KUed5neXTs1k8rtKEtvRjHMpMPTanckTm4ol8GYi0z8Rwq7FQqRr9D8LYXWqNW7sA9pG16GXrhQMBPWEYm4usxZe5QP36PnoV-15xZ6leQ7KF3woRScxPcPb7L81bACsT0GjBzIBg_dEMpLG0ckRl4w1LW8YfnYUrbmLK4gE5FwlD8hjJOBW4z_Tm_KGu8-gYE1zzb5KlOCeVGVcik2dUEP7U4zy20iDaBXLIDoD-ayZBKkwiw',
    parentNode: document.querySelector('#meeting-container'),
    configOverwrite: {
      brandingRoomAlias: 'anInterestingMeeting'
    },
    configOverwrite: { startWithAudioMuted: true },
    lang:'ar',
    devices: {
        audioInput: '<deviceLabel>',
        audioOutput: '<deviceLabel>',
        videoInput: '<deviceLabel>'
    },
    userInfo: {
        email: 'dev4.itsystematic@gmail.com',
        displayName: 'John Doe'
    },
  configOverwrite: {
    // disable the prejoin page
    prejoinPageEnabled: false,
  }  ,
  configOverwrite: {
    // disable the prejoin page
    toggleLobby: "enable-lobby",
  }  

    
                    // Make sure to include a JWT if you intend to record,
                    // make outbound calls or use any other premium features!
                    // jwt: "eyJraWQiOiJ2cGFhcy1tYWdpYy1jb29raWUtYzMwZTNkMWFiNTk3NGIxZThjMWQ2MTllOTBkYTMxNGUvYWFhMGM1LVNBTVBMRV9BUFAiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJqaXRzaSIsImlzcyI6ImNoYXQiLCJpYXQiOjE2OTYxNDc2MTYsImV4cCI6MTY5NjE1NDgxNiwibmJmIjoxNjk2MTQ3NjExLCJzdWIiOiJ2cGFhcy1tYWdpYy1jb29raWUtYzMwZTNkMWFiNTk3NGIxZThjMWQ2MTllOTBkYTMxNGUiLCJjb250ZXh0Ijp7ImZlYXR1cmVzIjp7ImxpdmVzdHJlYW1pbmciOmZhbHNlLCJvdXRib3VuZC1jYWxsIjpmYWxzZSwic2lwLW91dGJvdW5kLWNhbGwiOmZhbHNlLCJ0cmFuc2NyaXB0aW9uIjpmYWxzZSwicmVjb3JkaW5nIjpmYWxzZX0sInVzZXIiOnsiaGlkZGVuLWZyb20tcmVjb3JkZXIiOmZhbHNlLCJtb2RlcmF0b3IiOnRydWUsIm5hbWUiOiJUZXN0IFVzZXIiLCJpZCI6Imdvb2dsZS1vYXV0aDJ8MTAzMTc5NjgzMTM4NzE0NzAwMDg3IiwiYXZhdGFyIjoiIiwiZW1haWwiOiJ0ZXN0LnVzZXJAY29tcGFueS5jb20ifX0sInJvb20iOiIqIn0.j1BTSeUOY_NHkkON8qP-dSCE33mVclTLFL_WIUAX0ALkD30eN4c-bZRi6Ty-j-JC6Si0vwOmARyoMa7_Sg21MBtv1EHMfEN_AsVi39doBt3Er62ikiL5Noft3PfzQBnIEx-I4zosob0HP3jhW_zMhuVE_FI8PuSWCRX-CnmxxTPPQUXKGaHWeE5QyQ_KRcELca-78dHgLfEHx34G8WYs0feMhNILa_74xH0UyrUZAZZ7vaO5XtLIRSASd8lyIODw4ROaM_W_qoHwuMChna-HBF0_uUwilZ51MDNzkfWy4FhmyNlD3XY_luJEfNVFpwP-WPswM-v1oInOaxg5wHlEWQ"
    });
  }
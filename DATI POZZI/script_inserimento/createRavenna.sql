USE [Hera]
GO

/****** Object:  Table [dbo].[Ravenna]    Script Date: 4/12/2021 5:10:29 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Ravenna](
	[data_ora] [datetime] NOT NULL,
	[livello] [float] NOT NULL,
	[portata] [float] NOT NULL,
	[cod_pozzo] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Ravenna]  WITH CHECK ADD  CONSTRAINT [FK_Ravenna_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[Ravenna] CHECK CONSTRAINT [FK_Ravenna_coord]
GO



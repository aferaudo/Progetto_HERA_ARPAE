USE [Hera]
GO

/****** Object:  Table [dbo].[StatoPozzi]    Script Date: 5/28/2021 4:33:37 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[StatoPozzi](
	[cod_pozzo] [nvarchar](50) NOT NULL,
	[rete] [nvarchar](50) NOT NULL,
	[stato] [int] NOT NULL,
 CONSTRAINT [PK_StatoPozzi] PRIMARY KEY CLUSTERED 
(
	[cod_pozzo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[StatoPozzi]  WITH CHECK ADD  CONSTRAINT [FK_StatoPozzi_coord] FOREIGN KEY([cod_pozzo])
REFERENCES [dbo].[coord] ([cod_pozzo])
GO

ALTER TABLE [dbo].[StatoPozzi] CHECK CONSTRAINT [FK_StatoPozzi_coord]
GO


